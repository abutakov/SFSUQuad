"""empty message

Revision ID: 2bcaaedc7330
Revises: 6ffb951edac2
Create Date: 2019-12-11 20:50:19.701423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2bcaaedc7330'
down_revision = '6ffb951edac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('body', sa.String(length=40), nullable=True))
    op.drop_column('message', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('content', mysql.VARCHAR(length=40), nullable=True))
    op.drop_column('message', 'body')
    # ### end Alembic commands ###