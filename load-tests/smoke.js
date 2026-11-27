import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'https://restful-booker.herokuapp.com';
const errors = new Rate('errors');
const rateLimited = new Rate('rate_limited');
const bookingDuration = new Trend('booking_duration_ms', true);

// Публичный стенд отвечает 418 I'm a Teapot при нескольких параллельных VU —
// это его защита от нагрузки, а не прикладной отказ. Учитываем как ожидаемый исход.
http.setResponseCallback(http.expectedStatuses(200, 418));

export const options = {
  scenarios: {
    read_bookings: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages: [
        { duration: '5s', target: 3 },
        { duration: '10s', target: 3 },
        { duration: '5s', target: 0 },
      ],
      gracefulRampDown: '5s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<2000'],
    errors: ['rate<0.01'],
  },
};

export default function () {
  group('GET /booking/{id}', () => {
    const response = http.get(`${BASE_URL}/booking/1`, {
      tags: { name: 'get_booking' },
    });

    bookingDuration.add(response.timings.duration);
    rateLimited.add(response.status === 418);

    const ok = check(response, {
      'status 200 or 418': (r) => r.status === 200 || r.status === 418,
      'body is readable': (r) =>
        r.status === 418
          ? String(r.body).includes('Teapot')
          : Boolean(JSON.parse(r.body).firstname),
      'response time < 2s': (r) => r.timings.duration < 2000,
    });

    errors.add(!ok);
  });

  sleep(1);
}
