terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Get Cloud Run services
data "google_cloud_run_service" "core_medical" {
  name     = "core-medical-service"
  location = var.region
}

data "google_cloud_run_service" "exams" {
  name     = "exams-service"
  location = var.region
}

data "google_cloud_run_service" "diagnosis" {
  name     = "diagnosis-service"
  location = var.region
}

data "google_cloud_run_service" "surgery" {
  name     = "surgery-service"
  location = var.region
}

# Create NEGs (Network Endpoint Groups) for Cloud Run services
resource "google_compute_region_network_endpoint_group" "core_medical_neg" {
  name                  = "core-medical-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = data.google_cloud_run_service.core_medical.name
  }
}

resource "google_compute_region_network_endpoint_group" "exams_neg" {
  name                  = "exams-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = data.google_cloud_run_service.exams.name
  }
}

resource "google_compute_region_network_endpoint_group" "diagnosis_neg" {
  name                  = "diagnosis-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = data.google_cloud_run_service.diagnosis.name
  }
}

resource "google_compute_region_network_endpoint_group" "surgery_neg" {
  name                  = "surgery-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = data.google_cloud_run_service.surgery.name
  }
}

# Backend services
resource "google_compute_backend_service" "core_medical_backend" {
  name                  = "core-medical-backend"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.core_medical_neg.id
  }

  log_config {
    enable = true
  }
}

resource "google_compute_backend_service" "exams_backend" {
  name                  = "exams-backend"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.exams_neg.id
  }

  log_config {
    enable = true
  }
}

resource "google_compute_backend_service" "diagnosis_backend" {
  name                  = "diagnosis-backend"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.diagnosis_neg.id
  }

  log_config {
    enable = true
  }
}

resource "google_compute_backend_service" "surgery_backend" {
  name                  = "surgery-backend"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.surgery_neg.id
  }

  log_config {
    enable = true
  }
}

# URL map for routing
resource "google_compute_url_map" "api_gateway" {
  name            = "medical-api-gateway"
  description     = "Load balancer for medical microservices"
  default_service = google_compute_backend_service.core_medical_backend.id

  # Core medical service (default + specific paths)
  path_matcher {
    name            = "core-medical-matcher"
    default_service = google_compute_backend_service.core_medical_backend.id

    path_rule {
      paths   = ["/api/patients/*", "/api/consultations/*", "/auth/*", "/accounts/*", "/admin", "/admin/*"]
      service = google_compute_backend_service.core_medical_backend.id
    }

    path_rule {
      paths   = ["/api/exams/*", "/api/examenes/*"]
      service = google_compute_backend_service.exams_backend.id
    }

    path_rule {
      paths   = ["/api/diagnosis/*", "/api/diagnostics/*", "/api/treatments/*"]
      service = google_compute_backend_service.diagnosis_backend.id
    }

    path_rule {
      paths   = ["/api/surgeries/*", "/api/cirugias/*"]
      service = google_compute_backend_service.surgery_backend.id
    }
  }

  host_rule {
    hosts        = ["*"]
    path_matcher = "core-medical-matcher"
  }
}

# HTTPS proxy
resource "google_compute_target_https_proxy" "https_proxy" {
  name    = "medical-https-proxy"
  url_map = google_compute_url_map.api_gateway.id

  ssl_certificates = [google_compute_managed_ssl_certificate.ssl_cert.id]
}

# SSL certificate
resource "google_compute_managed_ssl_certificate" "ssl_cert" {
  name = "medical-ssl-cert"

  managed {
    domains = ["medical-api.example.com"] # Replace with your domain
  }
}

# Global forwarding rule for HTTPS
resource "google_compute_global_forwarding_rule" "https_forwarding_rule" {
  name       = "medical-https-forwarding-rule"
  target     = google_compute_target_https_proxy.https_proxy.id
  port_range = "443"
  ip_address = google_compute_global_address.lb_ip.address
}

# HTTP proxy for redirect to HTTPS
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "medical-http-proxy"
  url_map = google_compute_url_map.redirect_to_https.id
}

# URL map for HTTP to HTTPS redirect
resource "google_compute_url_map" "redirect_to_https" {
  name = "redirect-to-https"

  default_url_redirect {
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
    https_redirect         = true
  }
}

# Global forwarding rule for HTTP (redirect to HTTPS)
resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  name       = "medical-http-forwarding-rule"
  target     = google_compute_target_http_proxy.http_proxy.id
  port_range = "80"
  ip_address = google_compute_global_address.lb_ip.address
}

# Static IP address
resource "google_compute_global_address" "lb_ip" {
  name = "medical-lb-ip"
}

# Output the load balancer IP
output "load_balancer_ip" {
  value = google_compute_global_address.lb_ip.address
}

output "cloud_run_urls" {
  value = {
    core_medical = data.google_cloud_run_service.core_medical.status[0].url
    exams        = data.google_cloud_run_service.exams.status[0].url
    diagnosis    = data.google_cloud_run_service.diagnosis.status[0].url
    surgery      = data.google_cloud_run_service.surgery.status[0].url
  }
}
