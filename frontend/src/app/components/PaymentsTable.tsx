'use client';

import {Card, Title, useMantineTheme} from '@mantine/core';
import {Payment} from "@/app/typing/types";
import {MantineReactTable, MRT_ColumnDef} from "mantine-react-table";

export default function PaymentsTable({ payments }: { payments: Payment[] }) {
    const theme = useMantineTheme();

    const columns: MRT_ColumnDef<Payment>[] = [
        { accessorKey: 'type', header: 'Type' },
        { accessorKey: 'amount_cents', header: 'Amount', Cell: ({ cell }) =>
                `$${(cell.getValue<number>() / 100).toFixed(2)}` },
        { accessorKey: 'internal_account_id', header: 'Internal Account' },
        { accessorKey: 'external_account_id', header: 'External Account' },
        { accessorKey: 'external_payment_id', header: 'External Payment ID' },
    ];

    // Using inline styles here to access dynamic Mantine theme values.
    // Mantine theme tokens (like theme.colors.*) are not available in external CSS files,
    // so inline styling or createStyles() is the recommended approach for theme-aware styling.
    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ backgroundColor: theme.colors.primary[0] }}>
            <Title mb="md" style={{ color: theme.colors.secondary[0] }}>Payments</Title>
            <MantineReactTable columns={columns} data={payments} />
        </Card>
    );
}