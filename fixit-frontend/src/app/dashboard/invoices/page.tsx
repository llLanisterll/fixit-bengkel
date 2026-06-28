export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import InvoicesClient from "./InvoicesClient";
export default async function InvoicesPage() {
  const invoices = await fetchAPI("/invoices").catch(() => []);
  return <InvoicesClient invoices={JSON.parse(JSON.stringify(invoices))} />;
}
