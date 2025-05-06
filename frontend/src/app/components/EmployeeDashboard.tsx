'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import PaymentsTable from "@/app/components/PaymentsTable";
import TransactionsTable from "@/app/components/TransactionsTable";
import {Box, Stack, Title, useMantineTheme} from "@mantine/core";

export default function EmployeeDashboard() {
    const [payments, setPayments] = useState([]);
    const [transactions, setTransactions] = useState([]);
    const theme = useMantineTheme();

    useEffect(() => {
        axios.get('http://localhost:8000/api/payments').then((res) => setPayments(res.data));
        axios.get('http://localhost:8000/api/transactions').then((res) => setTransactions(res.data));
    }, []);

    // Using inline styles here to access dynamic Mantine theme values.
    // Mantine theme tokens (like theme.colors.*) are not available in external CSS files,
    // so inline styling or createStyles() is the recommended approach for theme-aware styling.
    return (
        <Box p="xl" style={{ backgroundColor: theme.colors.secondary[0] }}>
            <Stack spacing="xl">
                <Title order={1} style={{ color: theme.colors.primary[0] }}>Employee Dashboard</Title>
                <PaymentsTable payments={payments} />
                <TransactionsTable transactions={transactions} />
            </Stack>
        </Box>
    );
}