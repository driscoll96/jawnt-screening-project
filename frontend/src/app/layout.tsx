'use client';

import { MantineProvider } from '@mantine/core';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>
                <MantineProvider
                    withGlobalStyles
                    withNormalizeCSS
                    theme={{
                        colors: {
                            primary: ['#ff6124'],
                            secondary: ['#fff5f2'],
                        },
                        primaryColor: 'primary',
                    }}
                >
                    {children}
                </MantineProvider>
            </body>
        </html>
    );
}