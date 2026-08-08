# CarterFlare M365

## Goal

Stand up a Microsoft 365 tenant across multiple domains under the "CarterFlare" umbrella on Cloudflare.

Status: in-progress
Progress: n/a
Next Step: Finalize `carterlab.cloud` as the primary domain and verify catch-all mail routing to `inbox@cartermailbox.me`.

## Stack

- Microsoft 365
- Cloudflare DNS

## Details

- Multiple domains are managed under Cloudflare as "CarterFlare".
- `carterlab.cloud` is the target primary domain.
- Catch-all mail routes to `inbox@cartermailbox.me`.

## Related

- Admin console work here (M365/Exchange/Cloudflare) should follow detailed manual runbooks rather than automation scripts — see [`ai/profile.md`](../../../ai/profile.md).
