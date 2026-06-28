export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import SparepartsClient from "./SparepartsClient";
export default async function SparepartsPage() {
  const spareparts = await fetchAPI("/spareparts").catch(() => []);
  return <SparepartsClient spareparts={JSON.parse(JSON.stringify(spareparts))} />;
}
