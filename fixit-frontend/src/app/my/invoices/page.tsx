export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { FileText } from "lucide-react";
import PayInvoiceButton from "./PayInvoiceButton";

export default async function InvoicesPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  const userId = Number(session.user.id);
  const allInvoices = await fetchAPI("/invoices").catch(() => []);
  const invoices = allInvoices.filter((i: any) => i.booking?.userId === userId);

  return (
    <>
      <div className="page-header"><div><h1><FileText size={24} style={{ display: "inline", marginRight: "8px" }} />Invoice Saya</h1><p>{invoices.length} invoice</p></div></div>
      {invoices.length === 0 ? (
        <div className="card"><div className="empty-state"><div className="icon">📄</div><h3>Belum ada invoice</h3></div></div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {invoices.map((inv: any) => (
            <div key={inv.id} className="card">
              <div className="flex items-center justify-between" style={{ flexWrap: "wrap", gap: "12px" }}>
                <div>
                  <div style={{ fontWeight: 700, marginBottom: "4px" }}>{inv.invoiceNumber}</div>
                  <div style={{ fontSize: "13px", color: "var(--text-muted)" }}>{inv.booking?.bookingCode} • {inv.booking.vehicle.brand} {inv.booking.vehicle.model}</div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>{new Date(inv.createdAt).toLocaleDateString("id-ID")}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: "20px", fontWeight: 800, color: "var(--accent)" }}>Rp {inv.grandTotal.toLocaleString("id-ID")}</div>
                  <span className={`badge badge-${inv.paymentStatus.toLowerCase()}`}>{inv.paymentStatus}</span>
                  {inv.paymentMethod && <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}>{inv.paymentMethod}</div>}
                  {inv.paymentStatus === "UNPAID" && <PayInvoiceButton invoiceId={inv.id} />}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
