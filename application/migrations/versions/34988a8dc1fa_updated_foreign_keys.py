"""updated foreign keys

Revision ID: 34988a8dc1fa
Revises: e381c278b15a
Create Date: 2019-12-12 01:36:45.596356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34988a8dc1fa'
down_revision = 'e381c278b15a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('hash_id', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_hash_id'), 'user', ['hash_id'], unique=True)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=True),
    sa.Column('body', sa.String(length=240), nullable=True),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_email', sa.Integer(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=True),
    sa.Column('sender', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['post'], ['post.id'], ),
    sa.ForeignKeyConstraint(['sender'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_user_hash_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
