export interface Payment {
    id: number;
    type: string;
    external_account_id: number;
    internal_account_id: number;
    external_payment_id: string;
    amount_cents: number;
}

export interface Transaction {
    id: number;
    debit_card_id: number;
    external_payment_id: number;
    merchant_name: string;
    amount_cents: number;
}