"""empty message

Revision ID: 8a0bc5d2a79f
Revises: 
Create Date: 2019-12-17 00:38:41.149170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a0bc5d2a79f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('body', table_name='message')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('body', 'message', ['body'], unique=True)
    # ### end Alembic commands ###