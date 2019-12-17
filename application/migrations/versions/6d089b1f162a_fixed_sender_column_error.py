"""Fixed sender column error

Revision ID: 6d089b1f162a
Revises: 081deebca4c2
Create Date: 2019-12-12 00:57:40.693490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d089b1f162a'
down_revision = '081deebca4c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('sender', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'message', 'user', ['sender'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'sender')
    # ### end Alembic commands ###
