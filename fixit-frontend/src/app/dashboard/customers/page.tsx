export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import CustomersClient from "./CustomersClient";

export default async function CustomersPage() {
  const customers = await fetchAPI("/users").catch(() => []);
  return <CustomersClient customers={customers} />;
}
