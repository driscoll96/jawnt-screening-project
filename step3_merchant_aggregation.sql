-- SQL Query for Step 3 of the technical screening
-- Aggregates total funds paid to merchants by debit card transactions
-- Returns merchant names with the summed transaction amounts in USD

SELECT
  merchant_name,
  SUM(amount_cents) / 100.0 AS total_amount_usd
FROM
  organization_employee_account_debit_card_transaction
GROUP BY
  merchant_name
ORDER BY
  total_amount_usd DESC;