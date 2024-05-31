"""Alter password_hash size in employee table

Revision ID: 0647da4581ec
Revises: c11bec4cede9
Create Date: 2024-05-30 13:36:29.913347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0647da4581ec'
down_revision = 'c11bec4cede9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('employee', 'password_hash',
                    existing_type=sa.String(length=128),
                    type_=sa.String(length=256),
                    existing_nullable=True)


def downgrade():
    pass
