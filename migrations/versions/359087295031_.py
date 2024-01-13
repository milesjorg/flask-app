"""empty message

Revision ID: 359087295031
Revises: 545d158182c1
Create Date: 2024-01-12 12:46:10.905522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359087295031'
down_revision = '545d158182c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('base_game_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('time_start', sa.DateTime(), nullable=True),
    sa.Column('lap_splits', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('top_speed', sa.Float(), nullable=True),
    sa.Column('place_finished', sa.String(), nullable=True),
    sa.Column('play_duration', sa.Interval(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('high_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('base_game_data')
    op.drop_table('users')
    # ### end Alembic commands ###
