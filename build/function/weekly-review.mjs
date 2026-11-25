/* The Friday website review.
 *
 * Every Friday at 7am UTC (7am in winter, 8am in summer) this emails Jonathan
 * the week from Friday to Thursday: visits, page views, enquiries, the phone and
 * WhatsApp taps, where visitors came from, what they clicked and how far they
 * got with the forms, each compared with the week before. The numbers come from
 * the visit counter and the form function, through the site-stats store.
 *
 * Pressing "Run now" on this function in Netlify at any other time sends a test
 * copy covering the seven days up to and including today, with "Test" in the
 * subject. A test run never stops the real Friday one from going.
 */
import { getStore } from '@netlify/blobs';

// __REVIEW_LIB__

/* The schedule fires at 7am UTC on Friday. Anything outside a short window
   around that is somebody pressing Run now. */
function onSchedule(now) {
  const mins = now.getUTCHours() * 60 + now.getUTCMinutes();
  return now.getUTCDay() === 5 && mins >= 6 * 60 + 50 && mins <= 10 * 60;
}

export default async () => {
  const now = new Date();
  const store = getStore({ name: 'site-stats', consistency: 'strong' });
  const scheduled = onSchedule(now);
  const end = scheduled ? dueWeek(now).end : londonDate(now);
  try {
    const result = await sendReview(store, { end, test: !scheduled, why: scheduled ? 'schedule' : 'run now' });
    console.log('weekly review (week ending ' + end + '):', result);
  } catch (err) {
    console.error('weekly review (week ending ' + end + ') failed:', err && err.message);
  }
};

export const config = { schedule: '0 7 * * 5' };
