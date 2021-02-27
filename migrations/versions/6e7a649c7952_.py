"""empty message

Revision ID: 6e7a649c7952
Revises: da7874eb445c
Create Date: 2021-02-26 21:02:25.706565

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6e7a649c7952'
down_revision = 'da7874eb445c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('hair_color', sa.String(length=20), nullable=False))
    op.add_column('people', sa.Column('height', sa.Float(), nullable=False))
    op.add_column('people', sa.Column('skin_color', sa.String(length=20), nullable=False))
    op.drop_column('people', 'climate')
    op.drop_column('people', 'population')
    op.drop_column('people', 'terrain')
    op.drop_column('people', 'diameter')
    op.add_column('planet', sa.Column('climate', sa.String(length=20), nullable=False))
    op.add_column('planet', sa.Column('diameter', sa.Float(), nullable=False))
    op.add_column('planet', sa.Column('population', sa.Integer(), nullable=False))
    op.add_column('planet', sa.Column('terrain', sa.String(length=20), nullable=False))
    op.drop_column('planet', 'hair_color')
    op.drop_column('planet', 'height')
    op.drop_column('planet', 'skin_color')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planet', sa.Column('skin_color', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('planet', sa.Column('height', mysql.FLOAT(), nullable=False))
    op.add_column('planet', sa.Column('hair_color', mysql.VARCHAR(length=20), nullable=False))
    op.drop_column('planet', 'terrain')
    op.drop_column('planet', 'population')
    op.drop_column('planet', 'diameter')
    op.drop_column('planet', 'climate')
    op.add_column('people', sa.Column('diameter', mysql.FLOAT(), nullable=False))
    op.add_column('people', sa.Column('terrain', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('people', sa.Column('population', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('people', sa.Column('climate', mysql.VARCHAR(length=20), nullable=False))
    op.drop_column('people', 'skin_color')
    op.drop_column('people', 'height')
    op.drop_column('people', 'hair_color')
    # ### end Alembic commands ###
