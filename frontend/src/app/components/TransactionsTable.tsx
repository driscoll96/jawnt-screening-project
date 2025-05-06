'use client';

import {Card, Title, useMantineTheme} from '@mantine/core';
import {Transaction} from "@/app/typing/types";
import {MantineReactTable, MRT_ColumnDef} from "mantine-react-table";

export default function TransactionsTable({ transactions }: { transactions: Transaction[] }) {
    const theme = useMantineTheme();

    const columns: MRT_ColumnDef<Transaction>[] = [
        {accessorKey: 'merchant_name', header: 'Merchant'},
        {
            accessorKey: 'amount_cents',
            header: 'Amount',
            Cell: ({cell}) => `$${(cell.getValue<number>() / 100).toFixed(2)}`
        },
        {accessorKey: 'debit_card_id', header: 'Debit Card ID'},
        {accessorKey: 'external_payment_id', header: 'External Payment ID'},
    ];

    // Using inline styles here to access dynamic Mantine theme values.
    // Mantine theme tokens (like theme.colors.*) are not available in external CSS files,
    // so inline styling or createStyles() is the recommended approach for theme-aware styling.
    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ backgroundColor: theme.colors.primary[0] }}>
            <Title mb="md" style={{ color: theme.colors.secondary[0] }}>Transactions</Title>
            <MantineReactTable columns={columns} data={transactions}/>
        </Card>
    );
}