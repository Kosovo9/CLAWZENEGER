/**
 * @name Lead Scanner
 * @description Scans messages for lead information and saves it to the database.
 * @version 1.0.0
 */

function lead_scanner(text) {
  const patterns = {
    email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
    phone: /(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}/g,
    budget: /(?:presupuesto|budget|precio|costo|cost)\s*[:=]?\s*[\d,.$€]+/gi,
    industry: /(?:industria|sector|negocio|business)\s*[:=]?\s*(\w+)/gi
  };

  const results = {
    emails: text.match(patterns.email) || [],
    phones: text.match(patterns.phone) || [],
    budgets: text.match(patterns.budget) || [],
    industries: [...text.matchAll(patterns.industry)].map(m => m[1])
  };

  if (results.emails.length > 0 || results.phones.length > 0) {
    // Logic to save lead to persistence layer could be added here
    return `Lead detected: ${JSON.stringify(results, null, 2)}`;
  }

  return "No lead information detected.";
}

module.exports = { lead_scanner };
