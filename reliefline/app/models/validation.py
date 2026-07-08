from app.extensions import db

class DistributionRecord(db.Model):
    __tablename__ = "distribution_records"

    distribution_id = db.Column(db.Integer, primary_key=True)
    barangay_id = db.Column(db.Integer, db.ForeignKey("barangays.barangay_id"), nullable=False)
    allocation_id = db.Column(db.Integer, db.ForeignKey("allocation_records.allocation_id"), nullable=False)
    quantity_released = db.Column(db.Integer, default=0)
    distribution_date = db.Column(db.Date, nullable=False)
    validation_type = db.Column(db.Enum("photo", "signature"), nullable=False)
    validation_file = db.Column(db.String(255), nullable=True)
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    status = db.Column(db.Enum("pending", "confirmed"), default="pending")