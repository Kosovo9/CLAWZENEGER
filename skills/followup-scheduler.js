/**
 * @name Follow-up Scheduler
 * @description Schedules automated follow-up reminders.
 * @version 1.0.0
 */

function schedule_followup(leadName, days) {
    const followUpDate = new Date();
    followUpDate.setDate(followUpDate.getDate() + (days || 3));

    return {
        lead: leadName,
        scheduledDate: followUpDate.toLocaleDateString(),
        status: "Scheduled",
        message: `Recordatorio programado para ${leadName} en ${days || 3} días (${followUpDate.toLocaleDateString()}).`
    };
}

module.exports = { schedule_followup };
