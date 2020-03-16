"""Added users, towns and districts tables.

Revision ID: 78f1e4e56f37
Revises: 
Create Date: 2020-03-15 18:46:13.212855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f1e4e56f37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('districts',
        sa.Column('district_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('parent_district_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['parent_district_id'], ['districts.district_id'], ),
        sa.PrimaryKeyConstraint('district_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('users',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('password_hash', sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('towns',
        sa.Column('town_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('district_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['district_id'], ['districts.district_id'], ),
        sa.PrimaryKeyConstraint('town_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('towns')
    op.drop_table('users')
    op.drop_table('districts')
    # ### end Alembic commands ###
