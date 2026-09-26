// ============================================================================
// SPEED-TO-LEAD AI WEBHOOK & AUTORESPONDER (60-SECOND INBOUND RESPONSE)
// Target Market: High-Ticket Clinics, Real Estate, B2B SaaS, Agencies
// Monetization: $500 Setup + $250/mo Retainer per Client
// ============================================================================

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var leadName = data.name || "Valued Lead";
    var leadEmail = data.email || "";
    var leadPhone = data.phone || "";
    var leadNeed = data.message || "General Inquiry";
    
    // 1. Log Lead to Central Master Google Sheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.appendRow([new Date(), leadName, leadEmail, leadPhone, leadNeed, "AUTOMATED_RESPONSE_SENT"]);
    
    // 2. Draft Instant High-Touch Confirmation via Gmail
    if (leadEmail) {
      var subject = "Fast confirmation regarding your inquiry - " + leadName;
      var body = "Hi " + leadName + ",\n\n" +
                 "Thank you for reaching out. We received your note regarding '" + leadNeed + "'.\n\n" +
                 "Our team is already reviewing your details. Would tomorrow at 11:30 AM or 3:00 PM work best for a quick 10-minute discovery call?\n\n" +
                 "Best regards,\nClient Growth Team";
      GmailApp.createDraft(leadEmail, subject, body);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "SUCCESS",
      message: "Lead captured, logged to Google Sheet, and instant draft generated."
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "ERROR",
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
