SHOW SERVER_ENCODING;

--SELECT * FROM stg.stock_history;
--SELECT * FROM stg.stock_balance_sheet;
--SELECT * FROM stg.stock_dividends_history;
--SELECT * FROM  stg.stock_info;

CREATE SCHEMA stg;

DROP TABLE IF EXISTS stg.stock_history;
DROP TABLE IF EXISTS stg.stock_dividends_history;
DROP TABLE IF EXISTS stg.stock_info;
DROP TABLE IF EXISTS stg.stock_balance_sheet;

CREATE TABLE IF NOT EXISTS stg.stock_history(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , ticker        VARCHAR(20)
    , date          date NOT NULL
    , "open"        NUMERIC NOT NULL
    , high          NUMERIC NOT NULL
    , low           NUMERIC NOT NULL
    , "close"       NUMERIC NOT NULL
    , volume        NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS stg.stock_dividends_history(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , date          date NOT NULL
    , ticker        VARCHAR(20) NOT NULL
    , dividends     NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS stg.stock_info(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , ticker        VARCHAR(20)
    , info          JSON
);

CREATE TABLE IF NOT EXISTS stg.stock_balance_sheet(
    id                                              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , date                                          DATE NOT NULL
    , ticker                                        VARCHAR(20) NOT NULL
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
);

-- У меня глючил sqlalchemy(utf error какой-то выдавал, я решить не смог быстро, проект важнее)  поэтому записал данные вот так, если что автоматизация за счет airflow 
COPY stg.stock_history(date, "open", high, low, "close", volume, ticker) 
FROM '\Users\Public\stg_stock_history.csv' DELIMITER  ',' CSV HEADER;

COPY stg.stock_dividends_history(date, dividends, ticker) 
FROM '\Users\Public\stg_stock_dividends_history.csv' DELIMITER  ',' CSV HEADER;

COPY stg.stock_info(info, ticker) 
FROM '\Users\Public\stg_stock_info.csv' DELIMITER  ',' CSV HEADER;


COPY stg.stock_balance_sheet(date,
                             ordinary_shares_number,
                             share_issued,
                             net_debt,
                             total_debt,
                             tangible_book_value,
                             invested_capital,
                             working_capital,
                             net_tangible_assets,
                             capital_lease_obligations,
                             common_stock_equity,
                             total_capitalization,
                             total_equity_gross_minority_interest,
                             stockholders_equity,
                             gains_losses_not_affecting_retained_earnings,
                             other_equity_adjustments,
                             retained_earnings,
                             capital_stock,
                             common_stock,
                             total_liabilities_net_minority_interest,
                             total_non_current_liabilities_net_minority_interest,
                             other_non_current_liabilities,
                             tradeand_other_payables_non_current,
                             non_current_deferred_liabilities,
                             non_current_deferred_revenue,
                             non_current_deferred_taxes_liabilities,
                             long_term_debt_and_capital_lease_obligation,
                             long_term_capital_lease_obligation,
                             long_term_debt,
                             current_liabilities,
                             other_current_liabilities,
                             current_deferred_liabilities,
                             current_deferred_revenue,
                             current_debt_and_capital_lease_obligation,
                             current_debt,
                             pensionand_other_post_retirement_benefit_plans_current,
                             payables_and_accrued_expenses,
                             payables,
                             total_tax_payable,
                             income_tax_payable,
                             accounts_payable,
                             total_assets,
                             total_non_current_assets,
                             other_non_current_assets,
                             investments_and_advances,
                             long_term_equity_investment,
                             goodwill_and_other_intangible_assets,
                             other_intangible_assets,
                             goodwill,
                             net_ppe,
                             accumulated_depreciation,
                             gross_ppe,
                             leases,
                             other_properties,
                             machinery_furniture_equipment,
                             buildings_and_improvements,
                             land_and_improvements,
                             properties,
                             current_assets,
                             other_current_assets,
                             hedging_assets_current,
                             inventory,
                             finished_goods,
                             work_in_process,
                             raw_materials,
                             receivables,
                             accounts_receivable,
                             allowance_for_doubtful_accounts_receivable,
                             gross_accounts_receivable,
                             cash_cash_equivalents_and_short_term_investments,
                             other_short_term_investments,
                             cash_and_cash_equivalents,
                             cash_equivalents,
                             cash_financial,
                             ticker,
                             treasury_shares_number,
                             current_capital_lease_obligation,
                             other_current_borrowings,
                             commercial_paper,
                             non_current_deferred_assets,
                             non_current_deferred_taxes_assets,
                             other_investments,
                             investmentin_financial_assets,
                             available_for_sale_securities,
                             other_receivables,
                             minority_interest,
                             preferred_stock,
                             derivative_product_liabilities,
                             construction_in_progress,
                             prepaid_assets,
                             treasury_stock,
                             additional_paid_in_capital,
                             current_accrued_expenses,
                             inventories_adjustments_allowances,
                             other_inventories,
                             investments_in_other_ventures_under_equity_method,
                             receivables_adjustments_allowances,
                             loans_receivable,
                             employee_benefits,
                             current_provisions,
                             interest_payable,
                             other_payable,
                             non_current_prepaid_assets,
                             preferred_securities_outside_stock_equity,
                             financial_assets,
                             trading_securities,
                             assets_held_for_sale_current,
                             dueto_related_parties_current,
                             duefrom_related_parties_current,
                             non_current_accrued_expenses,
                             long_term_provisions,
                             line_of_credit,
                             taxes_receivable,
                             preferred_shares_number,
                             preferred_stock_equity,
                             held_to_maturity_securities,
                             cash_cash_equivalents_and_federal_funds_sold,
                             liabilities_heldfor_sale_non_current,
                             current_deferred_assets,
                             financial_assets_designatedas_fair_value_through_profitor_loss_total,
                             restricted_cash,
                             other_equity_interest,
                             non_current_pension_and_other_postretirement_benefit_plans,
                             dividends_payable,
                             foreign_currency_translation_adjustments,
                             minimum_pension_liabilities,
                             unrealized_gain_loss,
                             non_current_note_receivables,
                             non_current_accounts_receivable,
                             defined_pension_benefit)
FROM '\Users\Public\stg_stock_balance_sheet.csv' DELIMITER  ',' CSV HEADER;


