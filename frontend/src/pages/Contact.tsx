import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useState } from "react";
import { submitContact } from "@/api";
import type { ContactForm } from "@/types";

export default function Contact() {
  const [form, setForm] = useState<ContactForm>({ name: "", email: "", subject: "", message: "" });
  const [sent, setSent] = useState(false);

  const mutation = useMutation({
    mutationFn: submitContact,
    onSuccess: () => setSent(true),
  });

  const set = (k: keyof ContactForm) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm((p) => ({ ...p, [k]: e.target.value }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(form);
  };

  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-2xl px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Get in Touch</h1>
          <p className="text-gray-500 dark:text-gray-400">Have a project in mind or want to chat? I&apos;d love to hear from you.</p>
        </motion.div>

        {sent ? (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="rounded-2xl border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 p-8 text-center">
            <p className="text-2xl mb-2">:white_check_mark:</p>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">Message sent!</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">I&apos;ll get back to you soon.</p>
          </motion.div>
        ) : (
          <motion.form
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            onSubmit={handleSubmit}
            className="space-y-5"
          >
            {mutation.isError && (
              <div className="rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 text-sm text-red-600 dark:text-red-400">
                Something went wrong. Please try again.
              </div>
            )}

            <div className="grid sm:grid-cols-2 gap-5">
              <Field label="Name" value={form.name} onChange={set("name")} required />
              <Field label="Email" value={form.email} onChange={set("email")} type="email" required />
            </div>
            <Field label="Subject" value={form.subject} onChange={set("subject")} required />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Message</label>
              <textarea
                value={form.message}
                onChange={set("message")}
                rows={6}
                required
                className="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 transition resize-none"
                placeholder="Tell me what's on your mind…"
              />
            </div>

            <button
              type="submit"
              disabled={mutation.isPending}
              className="w-full py-3.5 rounded-xl bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white font-medium text-sm transition-colors shadow-lg shadow-brand-600/20"
            >
              {mutation.isPending ? "Sending…" : "Send Message"}
            </button>
          </motion.form>
        )}
      </div>
    </main>
  );
}

function Field({
  label, value, onChange, type = "text", required,
}: { label: string; value: string; onChange: (e: React.ChangeEvent<HTMLInputElement>) => void; type?: string; required?: boolean }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        className="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 transition"
      />
    </div>
  );
}