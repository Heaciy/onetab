"""init

Revision ID: 671507f4446f
Revises: 
Create Date: 2023-08-13 17:34:58.304392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '671507f4446f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uuid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='public'
    )
    op.create_table('device',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uuid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='public'
    )
    op.create_table('group',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uuid', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('links', sa.JSON(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('device_id', sa.BigInteger(), nullable=True),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('(now())'), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['public.device.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group', schema='public')
    op.drop_table('device', schema='public')
    op.drop_table('user', schema='public')
    # ### end Alembic commands ###
