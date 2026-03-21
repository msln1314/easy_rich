"""add north money tables

Revision ID: add_north_money
Revises:
Create Date: 2026-03-21

"""

from alembic import op
import sqlalchemy as sa


revision = "add_north_money"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "stock_north_money",
        sa.Column("id", sa.Integer(), nullable=False, comment="主键ID"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="创建时间",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="更新时间",
        ),
        sa.Column("delete_datetime", sa.DateTime(), nullable=True, comment="删除时间"),
        sa.Column("is_delete", sa.Boolean(), nullable=False, comment="是否软删除"),
        sa.Column("trade_date", sa.DateTime(), nullable=False, comment="交易日期"),
        sa.Column(
            "sh_buy_amount", sa.Float(), nullable=True, comment="沪股通买入金额(元)"
        ),
        sa.Column(
            "sh_sell_amount", sa.Float(), nullable=True, comment="沪股通卖出金额(元)"
        ),
        sa.Column(
            "sh_net_amount", sa.Float(), nullable=True, comment="沪股通净买入金额(元)"
        ),
        sa.Column(
            "sz_buy_amount", sa.Float(), nullable=True, comment="深股通买入金额(元)"
        ),
        sa.Column(
            "sz_sell_amount", sa.Float(), nullable=True, comment="深股通卖出金额(元)"
        ),
        sa.Column(
            "sz_net_amount", sa.Float(), nullable=True, comment="深股通净买入金额(元)"
        ),
        sa.Column(
            "total_buy_amount", sa.Float(), nullable=True, comment="合计买入金额(元)"
        ),
        sa.Column(
            "total_sell_amount", sa.Float(), nullable=True, comment="合计卖出金额(元)"
        ),
        sa.Column(
            "total_net_amount", sa.Float(), nullable=True, comment="合计净买入金额(元)"
        ),
        sa.Column(
            "data_time", sa.DateTime(), nullable=True, comment="数据时间（采集时间）"
        ),
        sa.Column("data_from", sa.String(length=50), nullable=True, comment="数据来源"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trade_date", name="uk_north_money_trade_date"),
        comment="北向资金流向表",
    )
    op.create_index("idx_north_money_trade_date", "stock_north_money", ["trade_date"])
    op.create_index("idx_north_money_created_at", "stock_north_money", ["created_at"])

    op.create_table(
        "stock_north_money_realtime",
        sa.Column("id", sa.Integer(), nullable=False, comment="主键ID"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="创建时间",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="更新时间",
        ),
        sa.Column("delete_datetime", sa.DateTime(), nullable=True, comment="删除时间"),
        sa.Column("is_delete", sa.Boolean(), nullable=False, comment="是否软删除"),
        sa.Column("data_date", sa.DateTime(), nullable=False, comment="数据日期"),
        sa.Column(
            "sh_buy_amount", sa.Float(), nullable=True, comment="沪股通买入金额(元)"
        ),
        sa.Column(
            "sh_sell_amount", sa.Float(), nullable=True, comment="沪股通卖出金额(元)"
        ),
        sa.Column(
            "sh_net_amount", sa.Float(), nullable=True, comment="沪股通净买入金额(元)"
        ),
        sa.Column(
            "sz_buy_amount", sa.Float(), nullable=True, comment="深股通买入金额(元)"
        ),
        sa.Column(
            "sz_sell_amount", sa.Float(), nullable=True, comment="深股通卖出金额(元)"
        ),
        sa.Column(
            "sz_net_amount", sa.Float(), nullable=True, comment="深股通净买入金额(元)"
        ),
        sa.Column(
            "total_buy_amount", sa.Float(), nullable=True, comment="合计买入金额(元)"
        ),
        sa.Column(
            "total_sell_amount", sa.Float(), nullable=True, comment="合计卖出金额(元)"
        ),
        sa.Column(
            "total_net_amount", sa.Float(), nullable=True, comment="合计净买入金额(元)"
        ),
        sa.Column("data_time", sa.DateTime(), nullable=True, comment="数据时间"),
        sa.Column("data_from", sa.String(length=50), nullable=True, comment="数据来源"),
        sa.PrimaryKeyConstraint("id"),
        comment="实时北向资金表",
    )
    op.create_index(
        "idx_north_money_realtime_data_date",
        "stock_north_money_realtime",
        ["data_date"],
    )
    op.create_index(
        "idx_north_money_realtime_data_time",
        "stock_north_money_realtime",
        ["data_time"],
    )


def downgrade():
    op.drop_index(
        "idx_north_money_realtime_data_time", table_name="stock_north_money_realtime"
    )
    op.drop_index(
        "idx_north_money_realtime_data_date", table_name="stock_north_money_realtime"
    )
    op.drop_table("stock_north_money_realtime")
    op.drop_index("idx_north_money_created_at", table_name="stock_north_money")
    op.drop_index("idx_north_money_trade_date", table_name="stock_north_money")
    op.drop_table("stock_north_money")
