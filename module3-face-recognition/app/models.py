from typing import Any

from pydantic import BaseModel


class FaceEnrollRequest(BaseModel):
    """Request model for face enrollment."""

    user_id: str
    image: str  # Base64 encoded image
    camera_consent: bool = False


class FaceEnrollResponse(BaseModel):
    """Response model for face enrollment."""

    enrollment_successful: bool
    face_template_hash: str  # 64-char SHA-256 hex string
    quality_score: float  # 0.0 to 1.0
    details: dict[str, Any]


class FaceVerifyRequest(BaseModel):
    """Request model for face verification."""

    image: str  # Base64 encoded image
    reference_template_hash: str  # Hash from enrollment


class FaceVerifyResponse(BaseModel):
    """Response model for face verification."""

    match_passed: bool
    match_score: float  # 0.0 to 1.0
    match_threshold: float  # Default: 0.70
    face_detected: bool
    current_template_hash: str


class LivenessRequest(BaseModel):
    """Request model for liveness check."""

    challenge_response: str  # Base64 encoded image
    challenge_type: str = "blink"  # blink, head_turn, passive


class LivenessResponse(BaseModel):
    """Response model for liveness check."""

    liveness_passed: bool
    liveness_score: float  # 0.0 to 1.0
    liveness_threshold: float  # Default: 0.60
    face_embedding_hash: str
    details: dict[str, Any]


class GeolocationData(BaseModel):
    """Geolocation data for risk assessment."""

    latitude: float
    longitude: float
    accuracy: float


class RiskAssessRequest(BaseModel):
    """Request model for risk assessment."""

    liveness_score: float | None = None
    face_match_score: float | None = None
    device_signature: str | None = None
    device_public_key: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    geolocation: GeolocationData | None = None


class RiskAssessResponse(BaseModel):
    """Response model for risk assessment."""

    risk_score: float  # 0.0 to 1.0
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    pass_threshold: bool
    risk_threshold: float  # Default: 0.50
    signal_breakdown: dict[str, float]
    recommendations: list[str]
