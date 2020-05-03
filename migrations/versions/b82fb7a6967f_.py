"""empty message

Revision ID: b82fb7a6967f
Revises: 
Create Date: 2020-04-25 16:25:02.849506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b82fb7a6967f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('school', sa.Integer(), nullable=True),
    sa.Column('is_smoke', sa.Boolean(), nullable=True),
    sa.Column('has_car', sa.Boolean(), nullable=True),
    sa.Column('has_bike', sa.Boolean(), nullable=True),
    sa.Column('noise_Sen', sa.Integer(), nullable=True),
    sa.Column('wakeup', sa.Integer(), nullable=True),
    sa.Column('bedtime', sa.Integer(), nullable=True),
    sa.Column('partyFreq', sa.Integer(), nullable=True),
    sa.Column('visitorFreq', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_school'), 'user', ['school'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('allergies',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('name', 'user_id')
    )
    op.create_table('ghost_user',
    sa.Column('representer_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=False),
    sa.Column('last_name', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['representer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('representer_id', 'email'),
    sa.UniqueConstraint('email')
    )
    op.create_table('pets',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('name', 'user_id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_type', sa.Boolean(), nullable=True),
    sa.Column('allows_pet', sa.Boolean(), nullable=False),
    sa.Column('allowed_gender', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('image_1', sa.LargeBinary(), nullable=True),
    sa.Column('image_2', sa.LargeBinary(), nullable=True),
    sa.Column('image_3', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_post_type'), 'posts', ['post_type'], unique=False)
    op.create_table('lives',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.create_table('offcampus',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=60), nullable=False),
    sa.Column('state', sa.String(length=60), nullable=False),
    sa.Column('zipcode', sa.String(length=5), nullable=True),
    sa.Column('nParking', sa.Integer(), nullable=True),
    sa.Column('nRoom', sa.Integer(), nullable=True),
    sa.Column('nBathroom', sa.Integer(), nullable=True),
    sa.Column('nKitchen', sa.Integer(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('pet_allowed', sa.Boolean(), nullable=True),
    sa.Column('substance_free', sa.Boolean(), nullable=True),
    sa.Column('ac', sa.Boolean(), nullable=True),
    sa.Column('laundry', sa.Boolean(), nullable=True),
    sa.Column('dishwasher', sa.Boolean(), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_index(op.f('ix_offcampus_city'), 'offcampus', ['city'], unique=False)
    op.create_index(op.f('ix_offcampus_state'), 'offcampus', ['state'], unique=False)
    op.create_table('oncampus',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('college', sa.Integer(), nullable=False),
    sa.Column('dorm_1', sa.String(length=60), nullable=True),
    sa.Column('dorm_2', sa.String(length=60), nullable=True),
    sa.Column('dorm_3', sa.String(length=60), nullable=True),
    sa.Column('drawNo', sa.Integer(), nullable=True),
    sa.Column('nSingles', sa.Integer(), nullable=True),
    sa.Column('nDoubles', sa.Integer(), nullable=True),
    sa.Column('nTriples', sa.Integer(), nullable=True),
    sa.Column('nQuads', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_index(op.f('ix_oncampus_nDoubles'), 'oncampus', ['nDoubles'], unique=False)
    op.create_index(op.f('ix_oncampus_nQuads'), 'oncampus', ['nQuads'], unique=False)
    op.create_index(op.f('ix_oncampus_nSingles'), 'oncampus', ['nSingles'], unique=False)
    op.create_index(op.f('ix_oncampus_nTriples'), 'oncampus', ['nTriples'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_oncampus_nTriples'), table_name='oncampus')
    op.drop_index(op.f('ix_oncampus_nSingles'), table_name='oncampus')
    op.drop_index(op.f('ix_oncampus_nQuads'), table_name='oncampus')
    op.drop_index(op.f('ix_oncampus_nDoubles'), table_name='oncampus')
    op.drop_table('oncampus')
    op.drop_index(op.f('ix_offcampus_state'), table_name='offcampus')
    op.drop_index(op.f('ix_offcampus_city'), table_name='offcampus')
    op.drop_table('offcampus')
    op.drop_table('lives')
    op.drop_index(op.f('ix_posts_post_type'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('pets')
    op.drop_table('ghost_user')
    op.drop_table('allergies')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_school'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###