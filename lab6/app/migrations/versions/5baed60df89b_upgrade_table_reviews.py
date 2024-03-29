"""upgrade table reviews

Revision ID: 5baed60df89b
Revises: 2634b68e185a
Create Date: 2023-06-13 21:38:14.933025

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5baed60df89b'
down_revision = '2634b68e185a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.create_foreign_key(op.f('fk_reviews_rating_grades'), 'reviews', 'grades', ['rating'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_reviews_rating_grades'), 'reviews', type_='foreignkey')
    op.alter_column('reviews', 'rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###
