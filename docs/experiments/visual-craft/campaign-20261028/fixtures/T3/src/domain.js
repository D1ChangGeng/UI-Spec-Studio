/**
 * IMMUTABLE FIXTURE DOMAIN.
 * These are fictional research sources authored for this local UI exercise.
 * No network, credentials, API keys, or backend are needed.
 */

export const SOURCE_SUMMARIES = Object.freeze([
  { id: 'heat-mapping', shortLabel: 'Osei · 2024', title: 'Reading heat at street level' },
  { id: 'shade-access', shortLabel: 'Park · 2023', title: 'The distance to shade' },
  { id: 'night-cooling', shortLabel: 'Rivera · 2025', title: 'When the city does not cool' },
]);

const RECORDS = {
  'heat-mapping': {
    id: 'heat-mapping',
    title: 'Reading heat at street level',
    subtitle: 'What block-by-block observations reveal about an uneven summer',
    authors: ['Ama Osei', 'Milan Shah'],
    publication: 'Urban Field Notes',
    date: 'June 18, 2024',
    year: '2024',
    kind: 'Field report',
    readingMinutes: 7,
    pages: '12–29',
    citation: 'Osei, A., & Shah, M. (2024). Reading heat at street level. Urban Field Notes, 8(2), 12–29.',
    url: 'https://example.org/margin-fixture/heat-mapping',
    tags: ['Street temperature', 'Observation', 'Urban form'],
    summary: 'Repeated walks through six contrasting neighborhoods show why a citywide temperature cannot describe the heat a person actually encounters. Exposure shifts with shade, surfaces, waiting time, and the route available to a walker.',
    keyQuote: 'The useful unit of heat exposure is often a journey, not a weather station.',
    relevance: 'Supports the notebook’s distinction between average air temperature and the lived experience of moving through a city.',
    sections: [
      {
        heading: 'A city measured in short walks',
        paragraphs: [
          'The field team followed twelve walking routes through six neighborhoods during three periods of a hot day. Each route linked an everyday origin and destination: a home and a bus stop, a school and a shop, or a clinic and a public square. At regular intervals, observers recorded shade, pavement condition, wind, and the places where people stopped. The purpose was to describe a sequence of exposures rather than to assign a single temperature to an entire neighborhood.',
          'Conditions changed over distances that conventional city maps treat as negligible. A shaded side street could lead directly into an exposed intersection. A bus shelter offered a roof but little protection from the low afternoon sun. One small courtyard remained comfortable long after the adjacent sidewalk became difficult to occupy. These transitions mattered because walkers could not always choose a different route or travel at a different time.',
          'Measurements were paired with route diaries. Participants described where they slowed down, crossed the street for shade, or chose to wait indoors. The diaries made it possible to separate a place that was briefly uncomfortable from a place that interrupted a necessary trip. A short exposed section near a clinic had greater practical significance than a larger hot area that most participants could avoid.',
        ],
      },
      {
        heading: 'The limits of a neighborhood average',
        paragraphs: [
          'A neighborhood mean can conceal both useful refuges and concentrated burdens. The field observations did not suggest abandoning broad temperature maps; they showed that those maps answer a different question. An average helps identify where investment may be needed. A route-level account helps determine what that investment should change for someone leaving home on a hot afternoon.',
          'Shade was most valuable where it coincided with unavoidable waiting. Crossings, transit stops, school gates, and clinic entrances emerged repeatedly in the diaries. A tree canopy elsewhere in the same block did not compensate for an exposed waiting area if the person could not leave the queue. Spatial proximity was therefore an incomplete measure of access.',
          'The team also observed a timing problem. A street that appeared well shaded in the morning could become exposed during the hours when school pickup and errands were most common. A useful public map would show how protection changes during the day, or at least identify the period represented by each observation.',
        ],
      },
      {
        heading: 'From observations to decisions',
        paragraphs: [
          'The report recommends combining repeated walks with a small set of resident-defined routes. This approach keeps the work manageable while preserving the relationship between an intervention and the activity it supports. The question becomes whether a person can reach the bus, buy groceries, or visit a neighbor with fewer difficult stretches along the way.',
          'The authors caution that the study covers a limited set of weather conditions and does not establish health outcomes. Its contribution is a practical method for noticing exposure that can disappear in aggregate data. Repeating the walks after a shade or pavement intervention would provide an immediate, legible account of what changed and what remains unresolved.',
        ],
      },
    ],
  },
  'shade-access': {
    id: 'shade-access',
    title: 'The distance to shade',
    subtitle: 'Access, opening hours, and the everyday geography of cool places',
    authors: ['Hana Park'],
    publication: 'Civic Landscapes Review',
    date: 'September 7, 2023',
    year: '2023',
    kind: 'Research essay',
    readingMinutes: 6,
    pages: '41–56',
    citation: 'Park, H. (2023). The distance to shade. Civic Landscapes Review, 14(3), 41–56.',
    url: 'https://example.org/margin-fixture/shade-access',
    tags: ['Public space', 'Access', 'Shade networks'],
    summary: 'An examination of neighborhood shade argues that proximity is only one part of access. A useful cool place must also be reachable, open, welcoming, and compatible with the routines of the people who need it.',
    keyQuote: 'A cool place on a map is not yet a cool place someone can use.',
    relevance: 'Adds practical conditions to the notebook’s idea of a connected network of cool routes and places.',
    sections: [
      {
        heading: 'Near is not the same as accessible',
        paragraphs: [
          'Maps of public green space commonly draw a circle around a park and count the residents within it. That measure is helpful for comparing large areas, but it treats the trip as frictionless. A person may live close to a shaded park and still face an exposed arterial road, a steep path, or an entrance far from the apparent edge of the site. The distance that matters is the distance along a route a person can actually take.',
          'The essay follows several ordinary trips to illustrate this difference. A caregiver traveling with a stroller selects a longer route to avoid steps. An older resident chooses a bench near a shop because it offers both shade and a familiar place to ask for help. A teenager avoids a nominally public courtyard because its signs and security presence suggest that lingering is unwelcome. Each example complicates the simple question of whether shade is nearby.',
          'Access also changes with time. School grounds may contain substantial tree cover but close during the hottest hours of a weekend. A library may be comfortable indoors but require a trip that is difficult in the afternoon. A park with no evening lighting may cease to be a usable option just as its temperature becomes tolerable.',
        ],
      },
      {
        heading: 'Small places within ordinary routines',
        paragraphs: [
          'The author proposes thinking about cool places as part of daily routines. A successful refuge does not always need to be a destination. It may be a shaded seat beside a grocery store, a covered edge of a playground, or a drinking fountain on the route between a transit stop and housing. These modest spaces can make an existing trip easier without asking a person to make an additional journey.',
          'This perspective shifts attention from the total area of canopy to the relationships among places. A series of small shaded intervals can support movement through a neighborhood even when no single park is large. Conversely, a large green space can have limited everyday value if the surrounding routes are difficult or the entrances do not align with where people come from.',
          'Maintenance is part of access. A damaged bench, an unreliable fountain, or a locked gate can turn an apparently complete network into a broken one. The essay recommends recording these details alongside physical shade coverage because they determine whether the intended benefit is available on a given day.',
        ],
      },
      {
        heading: 'A more useful public inventory',
        paragraphs: [
          'A neighborhood inventory could describe each cool place with a few plain-language attributes: where to enter, when it is open, whether there is seating, whether water is available, and which routes connect to it. The information should be easy to update, because operating conditions change more quickly than a tree canopy map.',
          'The essay does not offer a universal access score. It argues for making assumptions visible and testing them with the people whose routines an intervention is intended to support. The resulting map may be less tidy than a set of equal-radius circles, but it is more likely to explain why a well-placed investment is used, or why it is not.',
        ],
      },
    ],
  },
  'night-cooling': {
    id: 'night-cooling',
    title: 'When the city does not cool',
    subtitle: 'Nighttime heat, housing, and the recovery hours between hot days',
    authors: ['Elena Rivera', 'Noah Bell'],
    publication: 'Built Environment Working Papers',
    date: 'February 12, 2025',
    year: '2025',
    kind: 'Working paper',
    readingMinutes: 8,
    pages: '1–22',
    citation: 'Rivera, E., & Bell, N. (2025). When the city does not cool. Built Environment Working Papers, 25-04, 1–22.',
    url: 'https://example.org/margin-fixture/night-cooling',
    tags: ['Nighttime heat', 'Housing', 'Recovery'],
    summary: 'Interviews and indoor observations explore how warm nights extend the effects of a hot day. The paper connects building conditions with household choices and asks how public heat responses can account for the hours after sunset.',
    keyQuote: 'Sunset changes the light before it changes the conditions inside a home.',
    relevance: 'Broadens the notebook beyond outdoor daytime routes to the continuity of exposure and the importance of overnight recovery.',
    sections: [
      {
        heading: 'The hours after sunset',
        paragraphs: [
          'Public descriptions of heat often focus on the afternoon peak. Residents interviewed for this working paper described a different boundary: the point at which their homes became comfortable enough to rest. On some nights, that point arrived well after midnight. On others, it did not arrive before the next day began. The authors use these accounts to examine the continuity between daytime exposure and nighttime recovery.',
          'The study paired indoor observations with interviews in a varied group of homes. Its purpose was exploratory rather than representative. The records show how building orientation, stored heat, ventilation options, and household routines interacted over several consecutive warm days. Rooms with similar daytime readings sometimes cooled at very different rates after sunset.',
          'The household accounts also show why opening a window is not a simple or universal response. Noise, outdoor air conditions, insects, privacy, and concerns about security all influenced whether residents felt able to ventilate their homes. These constraints were particularly important for people whose bedrooms faced busy streets or shared outdoor spaces.',
        ],
      },
      {
        heading: 'Heat moves through a household routine',
        paragraphs: [
          'Participants described moving meals to a different room, postponing chores that generated heat, or changing where family members slept. These adaptations required space, time, and coordination. A household with several rooms had options that a household in a single small space did not. The apparent simplicity of an adaptation therefore concealed differences in the resources needed to carry it out.',
          'Warm nights affected the following day’s choices. Some residents postponed errands after poor sleep. Others left home early to spend time in a cooler public building, changing the hours in which transport and public facilities were most useful. The paper suggests that services planned only around the hottest afternoon period may miss these changes in routine.',
          'The authors distinguish immediate coping from durable improvement. A fan or a temporary cool room may provide practical relief, while building repairs and changes to the surrounding environment address conditions over a longer period. The two forms of response operate on different timescales and should be considered together.',
        ],
      },
      {
        heading: 'Connecting the home and the neighborhood',
        paragraphs: [
          'The paper argues that a heat response should connect indoor and outdoor conditions. An evening public space may be useful only if it is comfortable to reach and remains open when residents need it. Advice about ventilation should reflect the conditions outside the window. Information about services should be clear enough to use when people are tired and routines have already been disrupted.',
          'The findings are limited by the small sample and the short observation period. They do not establish a single building solution or a clinical threshold. Their value is to describe the hours that disappear when a heat event is represented only by a daytime maximum, and to identify questions for a more sustained study of recovery between hot days.',
        ],
      },
    ],
  },
};

function abortError() {
  return new DOMException('The source request was cancelled.', 'AbortError');
}

let failureDelivered = false;

/**
 * Resolves a fresh source record after 450 ms by default.
 * ?delay=1800 makes every request visibly slow (allowed range 0–10000 ms).
 * ?fault=once makes the first request that finishes fail, then retry succeeds.
 * Aborted requests do not consume the one-time failure.
 */
export function fetchSource(id, { signal } = {}) {
  const params = new URLSearchParams(window.location.search);
  const requestedDelay = Number(params.get('delay') ?? 450);
  const delay = Number.isFinite(requestedDelay) ? Math.min(10000, Math.max(0, requestedDelay)) : 450;

  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(abortError());
      return;
    }
    const onAbort = () => {
      window.clearTimeout(timer);
      reject(abortError());
    };
    const timer = window.setTimeout(() => {
      signal?.removeEventListener('abort', onAbort);
      if (signal?.aborted) {
        reject(abortError());
      } else if (!RECORDS[id]) {
        reject(new Error('This source could not be found.'));
      } else if (params.get('fault') === 'once' && !failureDelivered) {
        failureDelivered = true;
        reject(new Error('The source did not arrive. Please try again.'));
      } else {
        resolve(structuredClone(RECORDS[id]));
      }
    }, delay);
    signal?.addEventListener('abort', onAbort, { once: true });
  });
}

export function noteStorageKey(id) {
  return `margin:source-note:${id}`;
}

export function readSavedNote(id) {
  try {
    return window.localStorage.getItem(noteStorageKey(id)) ?? '';
  } catch {
    return '';
  }
}

export function saveSourceNote(id, text) {
  window.localStorage.setItem(noteStorageKey(id), text);
}
