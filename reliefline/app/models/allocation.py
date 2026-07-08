from app.extensions import db

class AllocationRecord(db.Model):
    __tablename__ = "allocation_records"

    allocation_id = db.Column(db.Integer, primary_key=True)
    barangay_id = db.Column(db.Integer, db.ForeignKey("barangays.barangay_id"), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("offices.office_id"), nullable=False)
    predicted_quantity = db.Column(db.Integer, default=0)
    allocated_quantity = db.Column(db.Integer, default=0)
    historical_allocation = db.Column(db.Integer, default=0)
    allocation_date = db.Column(db.Date, nullable=False)
    disaster_event = db.Column(db.String(150), nullable=True)
    status = db.Column(db.Enum("pending", "approved", "released"), default="pending")
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)


class PrepositionRecord(db.Model):
    __tablename__ = "preposition_records"

    preposition_id = db.Column(db.Integer, primary_key=True)
    from_office_id = db.Column(db.Integer, db.ForeignKey("offices.office_id"), nullable=False)
    to_barangay_id = db.Column(db.Integer, db.ForeignKey("barangays.barangay_id"), nullable=False)
    item_type = db.Column(db.Enum("food_pack"), default="food_pack")
    quantity = db.Column(db.Integer, default=0)
    preposition_date = db.Column(db.Date, nullable=False)
    disaster_event = db.Column(db.String(150), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)