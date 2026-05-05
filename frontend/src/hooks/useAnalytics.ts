import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { trackPageView } from "@/api";

const fingerprint = (() => {
  const key = "pf_fp";
  let fp = sessionStorage.getItem(key);
  if (!fp) {
    fp = Math.random().toString(36).slice(2) + Date.now().toString(36);
    sessionStorage.setItem(key, fp);
  }
  return fp;
})();

export function useAnalytics() {
  const { pathname } = useLocation();

  useEffect(() => {
    trackPageView(pathname, fingerprint);
  }, [pathname]);
}