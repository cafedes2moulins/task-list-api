"""empty message

Revision ID: a0c1da2f79f9
Revises: f3ca00b40eae
Create Date: 2022-11-09 08:10:41.964898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0c1da2f79f9'
down_revision = 'f3ca00b40eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###