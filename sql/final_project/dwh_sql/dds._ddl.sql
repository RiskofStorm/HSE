CREATE SCHEMA IF NOT EXISTS dds;


DROP TABLE IF EXISTS  dds.ticker CASCADE;
DROP TABLE IF EXISTS  dds.ticker_price_history CASCADE;
DROP TABLE IF EXISTS  dds.ticker_dividends_history CASCADE;
DROP TABLE IF EXISTS  dds.ticker_balance_sheet CASCADE;

CREATE TABLE IF NOT EXISTS dds.ticker(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , ticker        VARCHAR(20) UNIQUE NOT NULL
    , info          JSON
    , load_dt       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dds.ticker_price_history(
     id            BIGINT GENERATED ALWAYS AS IDENTITY
    , ticker_id     BIGINT NOT NULL
    , date          date NOT NULL
    , "open"        NUMERIC NOT NULL
    , high          NUMERIC NOT NULL
    , low           NUMERIC NOT NULL
    , "close"       NUMERIC NOT NULL
    , volume        NUMERIC NOT NULL
    , FOREIGN KEY (ticker_id) REFERENCES dds.ticker(id)
    , load_dt       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
PARTITION BY RANGE(date);


CREATE TABLE IF NOT EXISTS dds.ticker_dividends_history(
    id              BIGINT GENERATED ALWAYS AS IDENTITY
    , ticker_id     BIGINT NOT NULL
    , date          date NOT NULL
    , dividends     NUMERIC NOT NULL
    , FOREIGN KEY (ticker_id) REFERENCES dds.ticker(id)
    , load_dt       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
PARTITION BY RANGE(date);


CREATE TABLE IF NOT EXISTS dds.ticker_balance_sheet(
    id                                              BIGINT GENERATED ALWAYS AS IDENTITY
    , date                                          DATE NOT NULL
    , ticker_id                                     BIGINT NOT NULL
    , ordinary_shares_number                        NUMERIC
    , share_issued                                  NUMERIC
    , net_debt                                      NUMERIC
    , total_debt                                    NUMERIC
    , tangible_book_value                           NUMERIC
    , invested_capital                              NUMERIC
    , working_capital                               NUMERIC
    , net_tangible_assets                           NUMERIC
    , capital_lease_obligations                     NUMERIC
    , common_stock_equity                           NUMERIC
    , total_capitalization                          NUMERIC
    , total_equity_gross_minority_interest          NUMERIC
    , stockholders_equity                           NUMERIC
    , gains_losses_not_affecting_retained_earnings  NUMERIC
    , other_equity_adjustments                      NUMERIC
    , retained_earnings                             NUMERIC
    , capital_stock                                 NUMERIC
    , common_stock                                  NUMERIC
    , total_liabilities_net_minority_interest       NUMERIC
    , total_non_current_liabilities_net_minority_interest NUMERIC
    , other_non_current_liabilities                 NUMERIC
    , tradeand_other_payables_non_current           NUMERIC
    , non_current_deferred_liabilities              NUMERIC
    , non_current_deferred_revenue                  NUMERIC
    , non_current_deferred_taxes_liabilities        NUMERIC
    , long_term_debt_and_capital_lease_obligation   NUMERIC
    , long_term_capital_lease_obligation            NUMERIC
    , long_term_debt                                NUMERIC
    , current_liabilities                           NUMERIC
    , other_current_liabilities                     NUMERIC
    , current_deferred_liabilities                  NUMERIC
    , current_deferred_revenue                      NUMERIC
    , current_debt_and_capital_lease_obligation     NUMERIC
    , current_debt                                  NUMERIC
    , pensionand_other_post_retirement_benefit_plans_current NUMERIC
    , payables_and_accrued_expenses                 NUMERIC
    , payables                                      NUMERIC
    , total_tax_payable                             NUMERIC
    , income_tax_payable                            NUMERIC
    , accounts_payable                              NUMERIC
    , total_assets                                  NUMERIC
    , total_non_current_assets                      NUMERIC
    , other_non_current_assets                      NUMERIC
    , investments_and_advances                      NUMERIC
    , long_term_equity_investment                   NUMERIC
    , goodwill_and_other_intangible_assets          NUMERIC
    , other_intangible_assets                       NUMERIC
    , goodwill                                      NUMERIC
    , net_ppe                                       NUMERIC
    , accumulated_depreciation                      NUMERIC
    , gross_ppe                                     NUMERIC
    , leases                                        NUMERIC
    , other_properties                              NUMERIC
    , machinery_furniture_equipment                 NUMERIC
    , buildings_and_improvements                    NUMERIC
    , land_and_improvements                         NUMERIC
    , properties                                    NUMERIC
    , current_assets                                NUMERIC
    , other_current_assets                          NUMERIC
    , hedging_assets_current                        NUMERIC
    , inventory                                     NUMERIC
    , finished_goods                                NUMERIC
    , work_in_process                               NUMERIC
    , raw_materials                                 NUMERIC
    , receivables                                   NUMERIC
    , accounts_receivable                           NUMERIC
    , allowance_for_doubtful_accounts_receivable    NUMERIC
    , gross_accounts_receivable                     NUMERIC
    , cash_cash_equivalents_and_short_term_investments NUMERIC
    , other_short_term_investments                  NUMERIC
    , cash_and_cash_equivalents                     NUMERIC
    , cash_equivalents                              NUMERIC
    , cash_financial                                NUMERIC
    , treasury_shares_number                        NUMERIC
    , current_capital_lease_obligation              NUMERIC
    , other_current_borrowings                      NUMERIC
    , commercial_paper                              NUMERIC
    , non_current_deferred_assets                   NUMERIC
    , non_current_deferred_taxes_assets             NUMERIC
    , other_investments                             NUMERIC
    , investmentin_financial_assets                 NUMERIC
    , available_for_sale_securities                 NUMERIC
    , other_receivables                             NUMERIC
    , minority_interest                             NUMERIC
    , preferred_stock                               NUMERIC
    , derivative_product_liabilities                NUMERIC
    , construction_in_progress                      NUMERIC
    , prepaid_assets                                NUMERIC
    , treasury_stock                                NUMERIC
    , additional_paid_in_capital                    NUMERIC
    , current_accrued_expenses                      NUMERIC
    , inventories_adjustments_allowances            NUMERIC
    , other_inventories                             NUMERIC
    , investments_in_other_ventures_under_equity_method NUMERIC
    , receivables_adjustments_allowances            NUMERIC
    , loans_receivable                              NUMERIC
    , employee_benefits                             NUMERIC
    , current_provisions                            NUMERIC
    , interest_payable                              NUMERIC
    , other_payable                                 NUMERIC
    , non_current_prepaid_assets                    NUMERIC
    , preferred_securities_outside_stock_equity     NUMERIC
    , financial_assets                              NUMERIC
    , trading_securities                            NUMERIC
    , assets_held_for_sale_current                  NUMERIC
    , dueto_related_parties_current                 NUMERIC
    , duefrom_related_parties_current               NUMERIC
    , non_current_accrued_expenses                  NUMERIC
    , long_term_provisions                          NUMERIC
    , line_of_credit                                NUMERIC
    , taxes_receivable                              NUMERIC
    , preferred_shares_number                       NUMERIC
    , preferred_stock_equity                        NUMERIC
    , held_to_maturity_securities                   NUMERIC
    , cash_cash_equivalents_and_federal_funds_sold  NUMERIC
    , liabilities_heldfor_sale_non_current          NUMERIC
    , current_deferred_assets                       NUMERIC
    , financial_assets_designatedas_fair_value_through_profitor_loss_total NUMERIC
    , restricted_cash                               NUMERIC
    , other_equity_interest                         NUMERIC
    , non_current_pension_and_other_postretirement_benefit_plans NUMERIC
    , dividends_payable                             NUMERIC
    , foreign_currency_translation_adjustments      NUMERIC
    , minimum_pension_liabilities                   NUMERIC
    , unrealized_gain_loss                          NUMERIC
    , non_current_note_receivables                  NUMERIC
    , non_current_accounts_receivable               NUMERIC
    , defined_pension_benefit                       NUMERIC
    , FOREIGN KEY (ticker_id) REFERENCES dds.ticker(id)
    , load_dt                                       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
PARTITION BY LIST (EXTRACT (YEAR FROM date));





CREATE TABLE dds.ticker_price_history_default PARTITION OF  dds.ticker_price_history DEFAULT;
CREATE TABLE dds.ticker_price_history_2000 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2000-01-01') TO ('2000-12-31');
CREATE TABLE dds.ticker_price_history_2001 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2001-01-01') TO ('2001-12-31');
CREATE TABLE dds.ticker_price_history_2002 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2002-01-01') TO ('2002-12-31');
CREATE TABLE dds.ticker_price_history_2003 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2003-01-01') TO ('2003-12-31');
CREATE TABLE dds.ticker_price_history_2004 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2004-01-01') TO ('2004-12-31');
CREATE TABLE dds.ticker_price_history_2005 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2005-01-01') TO ('2005-12-31');
CREATE TABLE dds.ticker_price_history_2006 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2006-01-01') TO ('2006-12-31');
CREATE TABLE dds.ticker_price_history_2007 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2007-01-01') TO ('2007-12-31');
CREATE TABLE dds.ticker_price_history_2008 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2008-01-01') TO ('2008-12-31');
CREATE TABLE dds.ticker_price_history_2009 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2009-01-01') TO ('2009-12-31');
CREATE TABLE dds.ticker_price_history_2010 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2010-01-01') TO ('2010-12-31');
CREATE TABLE dds.ticker_price_history_2011 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2011-01-01') TO ('2011-12-31');
CREATE TABLE dds.ticker_price_history_2012 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2012-01-01') TO ('2012-12-31');
CREATE TABLE dds.ticker_price_history_2013 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2013-01-01') TO ('2013-12-31');
CREATE TABLE dds.ticker_price_history_2014 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2014-01-01') TO ('2014-12-31');
CREATE TABLE dds.ticker_price_history_2015 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2015-01-01') TO ('2015-12-31');
CREATE TABLE dds.ticker_price_history_2016 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2016-01-01') TO ('2016-12-31');
CREATE TABLE dds.ticker_price_history_2017 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2017-01-01') TO ('2017-12-31');
CREATE TABLE dds.ticker_price_history_2018 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2018-01-01') TO ('2018-12-31');
CREATE TABLE dds.ticker_price_history_2019 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2019-01-01') TO ('2019-12-31');
CREATE TABLE dds.ticker_price_history_2020 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2020-01-01') TO ('2020-12-31');
CREATE TABLE dds.ticker_price_history_2021 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2021-01-01') TO ('2021-12-31');
CREATE TABLE dds.ticker_price_history_2022 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2022-01-01') TO ('2022-12-31');
CREATE TABLE dds.ticker_price_history_2023 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2023-01-01') TO ('2023-12-31');
CREATE TABLE dds.ticker_price_history_2024 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2024-01-01') TO ('2024-12-31');
CREATE TABLE dds.ticker_price_history_2025 PARTITION OF dds.ticker_price_history FOR VALUES FROM ('2025-01-01') TO ('2025-12-31');
   
   
   
   
CREATE TABLE dds.ticker_dividends_history_default PARTITION OF  dds.ticker_dividends_history DEFAULT;
CREATE TABLE dds.ticker_dividends_history_2000 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2000-01-01') TO ('2000-12-01');
CREATE TABLE dds.ticker_dividends_history_2001 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2001-01-01') TO ('2001-12-01');
CREATE TABLE dds.ticker_dividends_history_2002 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2002-01-01') TO ('2002-12-01');
CREATE TABLE dds.ticker_dividends_history_2003 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2003-01-01') TO ('2003-12-01');
CREATE TABLE dds.ticker_dividends_history_2004 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2004-01-01') TO ('2004-12-01');
CREATE TABLE dds.ticker_dividends_history_2005 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2005-01-01') TO ('2005-12-01');
CREATE TABLE dds.ticker_dividends_history_2006 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2006-01-01') TO ('2006-12-01');
CREATE TABLE dds.ticker_dividends_history_2007 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2007-01-01') TO ('2007-12-01');
CREATE TABLE dds.ticker_dividends_history_2008 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2008-01-01') TO ('2008-12-01');
CREATE TABLE dds.ticker_dividends_history_2009 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2009-01-01') TO ('2009-12-01');
CREATE TABLE dds.ticker_dividends_history_2010 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2010-01-01') TO ('2010-12-01');
CREATE TABLE dds.ticker_dividends_history_2011 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2011-01-01') TO ('2011-12-01');
CREATE TABLE dds.ticker_dividends_history_2012 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2012-01-01') TO ('2012-12-01');
CREATE TABLE dds.ticker_dividends_history_2013 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2013-01-01') TO ('2013-12-01');
CREATE TABLE dds.ticker_dividends_history_2014 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2014-01-01') TO ('2014-12-01');
CREATE TABLE dds.ticker_dividends_history_2015 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2015-01-01') TO ('2015-12-01');
CREATE TABLE dds.ticker_dividends_history_2016 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2016-01-01') TO ('2016-12-01');
CREATE TABLE dds.ticker_dividends_history_2017 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2017-01-01') TO ('2017-12-01');
CREATE TABLE dds.ticker_dividends_history_2018 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2018-01-01') TO ('2018-12-01');
CREATE TABLE dds.ticker_dividends_history_2019 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2019-01-01') TO ('2019-12-01');
CREATE TABLE dds.ticker_dividends_history_2020 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2020-01-01') TO ('2020-12-01');
CREATE TABLE dds.ticker_dividends_history_2021 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2021-01-01') TO ('2021-12-01');
CREATE TABLE dds.ticker_dividends_history_2022 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2022-01-01') TO ('2022-12-01');
CREATE TABLE dds.ticker_dividends_history_2023 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2023-01-01') TO ('2023-12-01');
CREATE TABLE dds.ticker_dividends_history_2024 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2024-01-01') TO ('2024-12-01');
CREATE TABLE dds.ticker_dividends_history_2025 PARTITION OF dds.ticker_dividends_history FOR VALUES FROM ('2025-01-01') TO ('2025-12-01');



CREATE TABLE dds.ticker_balance_sheet_default PARTITION OF  dds.ticker_balance_sheet DEFAULT;
CREATE TABLE dds.ticker_balance_sheet_2000 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2000) ;
CREATE TABLE dds.ticker_balance_sheet_2001 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2001) ;
CREATE TABLE dds.ticker_balance_sheet_2002 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2002) ;
CREATE TABLE dds.ticker_balance_sheet_2003 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2003) ;
CREATE TABLE dds.ticker_balance_sheet_2004 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2004) ;
CREATE TABLE dds.ticker_balance_sheet_2005 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2005) ;
CREATE TABLE dds.ticker_balance_sheet_2006 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2006) ;
CREATE TABLE dds.ticker_balance_sheet_2007 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2007) ;
CREATE TABLE dds.ticker_balance_sheet_2008 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2008) ;
CREATE TABLE dds.ticker_balance_sheet_2009 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2009) ;
CREATE TABLE dds.ticker_balance_sheet_2010 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2010) ;
CREATE TABLE dds.ticker_balance_sheet_2011 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2011) ;
CREATE TABLE dds.ticker_balance_sheet_2012 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2012) ;
CREATE TABLE dds.ticker_balance_sheet_2013 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2013) ;
CREATE TABLE dds.ticker_balance_sheet_2014 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2014) ;
CREATE TABLE dds.ticker_balance_sheet_2015 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2015) ;
CREATE TABLE dds.ticker_balance_sheet_2016 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2016) ;
CREATE TABLE dds.ticker_balance_sheet_2017 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2017) ;
CREATE TABLE dds.ticker_balance_sheet_2018 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2018) ;
CREATE TABLE dds.ticker_balance_sheet_2019 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2019) ;
CREATE TABLE dds.ticker_balance_sheet_2020 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2020) ;
CREATE TABLE dds.ticker_balance_sheet_2021 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2021) ;
CREATE TABLE dds.ticker_balance_sheet_2022 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2022) ;
CREATE TABLE dds.ticker_balance_sheet_2023 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2023) ;
CREATE TABLE dds.ticker_balance_sheet_2024 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2024) ;
CREATE TABLE dds.ticker_balance_sheet_2025 PARTITION OF dds.ticker_balance_sheet FOR VALUES IN (2025) ;
