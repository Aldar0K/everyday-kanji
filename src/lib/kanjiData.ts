import type { Kanji } from './types'

/**
 * Seed curriculum: 20 fully-authored N5 kanji — readings, example words,
 * and stroke order for all of them.
 *
 * Stroke paths are real glyph data from the KanjiVG project
 * (https://kanjivg.tagaini.net, © KanjiVG contributors, CC BY-SA 3.0),
 * rescaled from KanjiVG's 109×109 viewBox into this app's shared 0-100
 * viewBox. Attribution must stay visible in the shipped app per the
 * license's share-alike terms — not yet added anywhere in the UI.
 */
export const KANJI_DATA: Kanji[] = [
  {
    day: 1,
    character: '一',
    meaning: 'один',
    kunReading: { kana: 'ひと(つ)', romaji: 'hito(tsu)' },
    onReading: { kana: 'イチ', romaji: 'ichi' },
    jlptLevel: 'N5',
    strokeCount: 1,
    exampleWords: [
      { word: '一つ', kana: 'ひとつ', romaji: 'hitotsu', translation: 'один (предмет)' },
      { word: '一月', kana: 'いちがつ', romaji: 'ichigatsu', translation: 'январь' },
      { word: '一人', kana: 'ひとり', romaji: 'hitori', translation: 'один человек' },
    ],
    strokes: [
      {
        d: 'M10.09,49.77c2.93,0.57,5.73,0.69,8.93,0.46c18.94-1.38,46.23-4.7,62.92-4.81c3.3-0.02,5.29,0.22,6.94,0.45',
        start: { x: 10.1, y: 49.8 },
        instruction: 'слева направо',
      },
    ],
    writingNote: 'Одна черта. Веди слева направо, ровно и спокойно.',
  },
  {
    day: 2,
    character: '二',
    meaning: 'два',
    kunReading: { kana: 'ふた(つ)', romaji: 'futa(tsu)' },
    onReading: { kana: 'ニ', romaji: 'ni' },
    jlptLevel: 'N5',
    strokeCount: 2,
    exampleWords: [
      { word: '二つ', kana: 'ふたつ', romaji: 'futatsu', translation: 'два (предмета)' },
      { word: '二月', kana: 'にがつ', romaji: 'nigatsu', translation: 'февраль' },
      { word: '二人', kana: 'ふたり', romaji: 'futari', translation: 'два человека' },
    ],
    strokes: [
      {
        d: 'M23.17,29.72c1.62,0.34,4.39,0.51,6.01,0.34c9.93-1.06,26.44-3.12,37.83-3.45c2.71-0.08,4.34,0.17,5.7,0.33',
        start: { x: 23.2, y: 29.7 },
        instruction: 'верхняя черта',
      },
      {
        d: 'M11.01,74.08c2.17,0.46,6.17,0.61,8.34,0.46c21.83-1.61,41.32-3.78,61.92-4.35c3.62-0.1,5.8,0.22,7.61,0.45',
        start: { x: 11.0, y: 74.1 },
        instruction: 'нижняя черта',
      },
    ],
    writingNote: 'Две черты. Сначала верхняя, потом нижняя — обе слева направо.',
  },
  {
    day: 3,
    character: '三',
    meaning: 'три',
    kunReading: { kana: 'み(っつ)', romaji: 'mi(ttsu)' },
    onReading: { kana: 'サン', romaji: 'san' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '三つ', kana: 'みっつ', romaji: 'mittsu', translation: 'три (предмета)' },
      { word: '三月', kana: 'さんがつ', romaji: 'sangatsu', translation: 'март' },
      { word: '三人', kana: 'さんにん', romaji: 'sannin', translation: 'три человека' },
    ],
    strokes: [
      {
        d: 'M25.23,21.7c2.83,0.67,5.77,0.33,8.62,0.06c9.36-0.92,24.77-2.7,35.75-3.28c2.81-0.15,5.59-0.18,8.39,0.21',
        start: { x: 25.2, y: 21.7 },
        instruction: 'верхняя черта',
      },
      {
        d: 'M26.38,50.59c2.87,0.7,5.93,0.39,8.84,0.18c9.2-0.66,21.99-2.41,31.86-2.86c2.48-0.11,5-0.15,7.46,0.28',
        start: { x: 26.4, y: 50.6 },
        instruction: 'средняя черта',
      },
      {
        d: 'M11.93,80.58c3.61,0.93,7.08,0.88,10.78,0.66c16.89-0.98,37.86-3.11,56.07-3.73c3.33-0.12,6.61-0.09,9.86,0.72',
        start: { x: 11.9, y: 80.6 },
        instruction: 'нижняя черта',
      },
    ],
    writingNote: 'Три черты подряд, сверху вниз: верхняя, средняя, нижняя. Каждая — слева направо.',
  },
  {
    day: 4,
    character: '十',
    meaning: 'десять',
    kunReading: { kana: 'とお', romaji: 'too' },
    onReading: { kana: 'ジュウ', romaji: 'juu' },
    jlptLevel: 'N5',
    strokeCount: 2,
    exampleWords: [
      { word: '十日', kana: 'とおか', romaji: 'tooka', translation: 'десятое число' },
      { word: '十月', kana: 'じゅうがつ', romaji: 'juugatsu', translation: 'октябрь' },
      { word: '五十', kana: 'ごじゅう', romaji: 'gojuu', translation: 'пятьдесят' },
    ],
    strokes: [
      {
        d: 'M10.9,46.77c2.92,0.82,6.07,0.56,9.06,0.32c18.28-1.45,41.5-4.37,58.15-5.34c3.53-0.21,6.63-0.06,10.09,0.51',
        start: { x: 10.9, y: 46.8 },
        instruction: 'горизонтальная, слева направо',
      },
      {
        d: 'M47.91,10.67c1.28,1.28,2.02,3.63,2.02,5.74c0,1.04-0.03,46.99-0.17,67.35c-0.03,3.63-0.06,6.27-0.07,7.41',
        start: { x: 47.9, y: 10.7 },
        instruction: 'вертикальная, сверху вниз',
      },
    ],
    writingNote: 'Две черты. Сначала горизонтальная слева направо, потом вертикальная сверху вниз через середину.',
  },
  {
    day: 5,
    character: '人',
    meaning: 'человек',
    kunReading: { kana: 'ひと', romaji: 'hito' },
    onReading: { kana: 'ジン', romaji: 'jin' },
    jlptLevel: 'N5',
    strokeCount: 2,
    exampleWords: [
      { word: '日本人', kana: 'にほんじん', romaji: 'nihonjin', translation: 'японец' },
      { word: '外人', kana: 'がいじん', romaji: 'gaijin', translation: 'иностранец' },
      { word: '大人', kana: 'おとな', romaji: 'otona', translation: 'взрослый' },
    ],
    strokes: [
      {
        d: 'M50,18.35c0.34,1.94,0.21,3.7-0.2,5.75C47.41,36.22,35.09,66.28,15.14,80.05',
        start: { x: 50.0, y: 18.4 },
        instruction: 'сверху вниз-влево',
      },
      {
        d: 'M42.2,49.77c5.61,5.5,23.4,20.4,32.59,27.27c3.36,2.5,6.37,4.26,10.53,5.07',
        start: { x: 42.2, y: 49.8 },
        instruction: 'сверху вниз-вправо',
      },
    ],
    writingNote: 'Две черты, как ноги идущего человека. Сначала длинная влево-вниз, потом короче — вправо-вниз.',
  },
  {
    day: 6,
    character: '大',
    meaning: 'большой',
    kunReading: { kana: 'おお(きい)', romaji: 'oo(kii)' },
    onReading: { kana: 'ダイ', romaji: 'dai' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '大きい', kana: 'おおきい', romaji: 'ookii', translation: 'большой' },
      { word: '大学', kana: 'だいがく', romaji: 'daigaku', translation: 'университет' },
      { word: '大好き', kana: 'だいすき', romaji: 'daisuki', translation: 'очень нравится' },
    ],
    strokes: [
      {
        d: 'M17.78,44.27c1.37,0.47,4.61,0.82,6.97,0.45C37.72,42.66,57.8,39.45,70.82,38.94c2.48-0.1,4.47-0.06,6.71,0.3',
        start: { x: 17.8, y: 44.3 },
        instruction: 'горизонтальная черта',
      },
      {
        d: 'M45.41,16.51c0.81,1.94,0.94,3.82,0.91,5.8C45.87,52.29,34.63,74.42,16.51,84.17',
        start: { x: 45.4, y: 16.5 },
        instruction: 'черта влево-вниз',
      },
      {
        d: 'M45.41,42.2c8.26,9.63,26.15,33.26,34.39,39.71c2.81,2.19,5.16,3.44,6.43,3.64',
        start: { x: 45.4, y: 42.2 },
        instruction: 'черта вправо-вниз',
      },
    ],
    writingNote: 'Три черты. Сначала горизонтальная, потом от центра — влево-вниз и вправо-вниз, как раскинутые руки.',
  },
  {
    day: 7,
    character: '木',
    meaning: 'дерево',
    kunReading: { kana: 'き', romaji: 'ki' },
    onReading: { kana: 'モク', romaji: 'moku' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '木曜日', kana: 'もくようび', romaji: 'mokuyoubi', translation: 'четверг' },
      { word: '木村', kana: 'きむら', romaji: 'kimura', translation: 'Кимура (фамилия)' },
      { word: '大木', kana: 'たいぼく', romaji: 'taiboku', translation: 'большое дерево' },
    ],
    strokes: [
      {
        d: 'M17.89,36.57c2.25,0.52,4.8,0.73,7.38,0.52C37.39,36.13,57.8,33.49,73.19,33.17c2.57-0.06,4.17,0.09,6.73,0.46',
        start: { x: 17.9, y: 36.6 },
        instruction: 'горизонтальная черта',
      },
      {
        d: 'M47.48,9.63c1.09,1.09,1.83,2.75,1.83,4.59c0,7.94,0,50.6-0.13,68.58c-0.03,3.84-0.06,6.56-0.1,7.57',
        start: { x: 47.5, y: 9.6 },
        instruction: 'вертикальная, сверху вниз',
      },
      {
        d: 'M46.56,36.24c0,1.03-0.56,2.24-1.3,3.62C38.3,52.75,24.5,67.83,14.45,73.62',
        start: { x: 46.6, y: 36.2 },
        instruction: 'черта влево-вниз',
      },
      {
        d: 'M50,35.78c4.24,5.5,21.1,23.62,29.14,31.75c2.08,2.1,4.23,4.03,6.87,5.17',
        start: { x: 50.0, y: 35.8 },
        instruction: 'черта вправо-вниз',
      },
    ],
    writingNote: 'Четыре черты: горизонтальная, вертикальная через неё, затем две черты-ветви вниз — влево и вправо.',
  },
  {
    day: 8,
    character: '川',
    meaning: 'река',
    kunReading: { kana: 'かわ', romaji: 'kawa' },
    onReading: { kana: 'セン', romaji: 'sen' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '川', kana: 'かわ', romaji: 'kawa', translation: 'река' },
      { word: '小川', kana: 'おがわ', romaji: 'ogawa', translation: 'ручей' },
      { word: '河川', kana: 'かせん', romaji: 'kasen', translation: 'реки (обобщённо)' },
    ],
    strokes: [
      {
        d: 'M24.97,23.56c0.83,1.44,1.08,3.17,1.09,4.93C26.15,39.91,26.15,63.3,15.95,77.2',
        start: { x: 25.0, y: 23.6 },
        instruction: 'левая черта',
      },
      {
        d: 'M49.31,21.68c0.86,0.86,1.29,2.17,1.29,3.58c0,0.53-0.01,26.13-0.07,38.27c-0.02,3.04-0.04,5.27-0.06,6.08',
        start: { x: 49.3, y: 21.7 },
        instruction: 'средняя черта',
      },
      {
        d: 'M78.5,14.34c1,1,1.61,2.4,1.61,3.9c0,0.68,0.21,42.99,0.08,60.66c-0.03,3.95-0.06,6.98-0.08,7.92',
        start: { x: 78.5, y: 14.3 },
        instruction: 'правая черта',
      },
    ],
    writingNote: 'Три вертикальные черты одна за другой, слева направо. Как берега и течение реки.',
  },
  {
    day: 9,
    character: '火',
    meaning: 'огонь',
    kunReading: { kana: 'ひ', romaji: 'hi' },
    onReading: { kana: 'カ', romaji: 'ka' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '火曜日', kana: 'かようび', romaji: 'kayoubi', translation: 'вторник' },
      { word: '花火', kana: 'はなび', romaji: 'hanabi', translation: 'фейерверк' },
      { word: '火山', kana: 'かざん', romaji: 'kazan', translation: 'вулкан' },
    ],
    strokes: [
      {
        d: 'M22.25,31.19c3,3.06,7.8,11.93,8.72,16.28',
        start: { x: 22.2, y: 31.2 },
        instruction: 'короткая черта, вверху слева',
      },
      {
        d: 'M76.15,25c0.46,1.27,0.2,2.51-0.46,3.9c-2.18,4.59-6.88,11.12-11.7,15.83',
        start: { x: 76.2, y: 25.0 },
        instruction: 'короткая черта, вверху справа',
      },
      {
        d: 'M48.17,13.07c0.92,1.15,1.38,2.86,1.38,4.59C49.54,63.3,36.35,73.39,19.27,83.94',
        start: { x: 48.2, y: 13.1 },
        instruction: 'длинная черта влево-вниз',
      },
      {
        d: 'M48.39,45.87c11.46,12.9,22.94,26.07,30.84,33.15c2.48,2.22,4.5,3.69,7.69,4.47',
        start: { x: 48.4, y: 45.9 },
        instruction: 'длинная черта вправо-вниз',
      },
    ],
    writingNote: 'Четыре черты. Сначала две короткие вверху, потом две длинные — влево-вниз и вправо-вниз.',
  },
  {
    day: 10,
    character: '日',
    meaning: 'солнце, день',
    kunReading: { kana: 'ひ', romaji: 'hi' },
    onReading: { kana: 'ニチ', romaji: 'nichi' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '日曜日', kana: 'にちようび', romaji: 'nichiyoubi', translation: 'воскресенье' },
      { word: '毎日', kana: 'まいにち', romaji: 'mainichi', translation: 'каждый день' },
      { word: '日本', kana: 'にほん', romaji: 'nihon', translation: 'Япония' },
    ],
    strokes: [
      {
        d: 'M28.9,22.48c1.03,1.03,1.6,2.52,1.6,4.36c0,1.47-0.15,34.96-0.08,49.08c0.02,3.5,0.05,5.83,0.08,6.19',
        start: { x: 28.9, y: 22.5 },
        instruction: 'левая вертикальная черта',
      },
      {
        d: 'M30.72,23.85c0.73-0.05,34.56-2.76,37.4-2.98c2.93-0.23,4.59,1.61,4.59,3.9c0,3.67-0.2,37.47-0.21,51.38c0,3.19,0,5.25,0,5.5',
        start: { x: 30.7, y: 23.9 },
        instruction: 'верх и правая сторона одной чертой',
      },
      {
        d: 'M31.39,50.69c7.14-0.46,32.94-2.29,40.42-2.52',
        start: { x: 31.4, y: 50.7 },
        instruction: 'средняя горизонтальная черта',
      },
      {
        d: 'M31.4,79.36c9.65-0.69,31.33-1.94,40.19-2.06',
        start: { x: 31.4, y: 79.4 },
        instruction: 'нижняя черта, закрывает',
      },
    ],
    writingNote: 'Четыре черты: левая сторона, затем верх и правая сторона одной чертой, потом средняя и нижняя линии.',
  },
  {
    day: 11,
    character: '月',
    meaning: 'луна, месяц',
    kunReading: { kana: 'つき', romaji: 'tsuki' },
    onReading: { kana: 'ゲツ', romaji: 'getsu' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '月曜日', kana: 'げつようび', romaji: 'getsuyoubi', translation: 'понедельник' },
      { word: '今月', kana: 'こんげつ', romaji: 'kongetsu', translation: 'этот месяц' },
      { word: '一月', kana: 'いちがつ', romaji: 'ichigatsu', translation: 'январь' },
    ],
    strokes: [
      {
        d: 'M31.42,14.91c0.92,0.92,1.36,2.18,1.38,3.67c0.35,30.84,2.18,54.48-10.09,67.2',
        start: { x: 31.4, y: 14.9 },
        instruction: 'левая черта',
      },
      {
        d: 'M33.26,17.43c3.78-0.57,28.89-4.39,30.5-4.59c3.67-0.46,5.05,1.03,5.05,4.36c0,2.53-0.46,45.18-0.46,63.76c0,11.93-5.73,3.67-8.03,1.61',
        start: { x: 33.3, y: 17.4 },
        instruction: 'верх, право и низ одной чертой',
      },
      {
        d: 'M34.17,34.86c9.4-1.38,25-3.44,33.26-4.13',
        start: { x: 34.2, y: 34.9 },
        instruction: 'первая внутренняя черта',
      },
      {
        d: 'M33.94,53.44c8.03-1.03,24.77-3.21,33.26-3.67',
        start: { x: 33.9, y: 53.4 },
        instruction: 'вторая внутренняя черта',
      },
    ],
    writingNote: 'Четыре черты: левая сторона, затем верх, право и низ одной чертой, потом две черты внутри.',
  },
  {
    day: 12,
    character: '山',
    meaning: 'гора',
    kunReading: { kana: 'やま', romaji: 'yama' },
    onReading: { kana: 'サン', romaji: 'san' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '火山', kana: 'かざん', romaji: 'kazan', translation: 'вулкан' },
      { word: '山道', kana: 'やまみち', romaji: 'yamamichi', translation: 'горная тропа' },
      { word: '富士山', kana: 'ふじさん', romaji: 'Fuji-san', translation: 'гора Фудзи' },
    ],
    strokes: [
      {
        d: 'M48.16,14.22c1.27,1.27,2.07,3.21,2.07,5.28c0,0.69-0.2,53.49-0.23,54.36',
        start: { x: 48.2, y: 14.2 },
        instruction: 'сверху вниз',
      },
      {
        d: 'M19.72,50c0.81,0.81,1.28,2.06,1.16,3.44c-0.53,6.41-0.92,14.68-2.29,21.1c-0.64,2.99,0.1,3.67,1.83,3.44c15.6-2.06,43.23-4.7,60.09-5.5',
        start: { x: 19.7, y: 50.0 },
        instruction: 'вниз и вправо',
      },
      {
        d: 'M81.87,44.95c0.86,0.86,1.5,2.18,1.39,3.9c-0.23,3.38-1.68,18.62-2.34,26.39c-0.2,2.42-0.36,4.14-0.41,4.57',
        start: { x: 81.9, y: 45.0 },
        instruction: 'правая стена',
      },
    ],
    writingNote: 'Три черты. Сначала середина, потом левая стена с дном, в конце — правая. Обведи пальцем по серому.',
  },

  {
    day: 13,
    character: '女',
    meaning: 'женщина',
    kunReading: { kana: 'おんな', romaji: 'onna' },
    onReading: { kana: 'ジョ', romaji: 'jo' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '女の子', kana: 'おんなのこ', romaji: 'onna no ko', translation: 'девочка' },
      { word: '女性', kana: 'じょせい', romaji: 'josei', translation: 'женщина (офиц.)' },
      { word: '彼女', kana: 'かのじょ', romaji: 'kanojo', translation: 'она, девушка' },
    ],
    strokes: [
      {
        d: 'M48.82,16.85c0.5,1.95,0.24,3.13-0.23,4.82C46.22,30.28,39.1,48.39,32.8,58.72c-1.28,2.08-0.92,3.21,0.92,3.21c10.67,0,26.11,6.86,35.62,15.06c2.35,2.03,4.29,4.14,5.66,6.28',
        start: { x: 48.8, y: 16.9 },
        instruction: 'дуга сверху вниз, потом вправо-вниз',
      },
      {
        d: 'M63.87,38.7c0.46,1.56,0.58,3.28-0.01,5.44C60.49,56.7,50.1,74.86,24.77,84.17',
        start: { x: 63.9, y: 38.7 },
        instruction: 'сверху справа вниз-влево',
      },
      {
        d: 'M12.73,46.27c3.19,1.28,6.66,0.78,9.98,0.49c17.91-1.56,38.57-3.74,55.61-4.25c3.36-0.1,6.61-0.09,9.74,1.3',
        start: { x: 12.7, y: 46.3 },
        instruction: 'горизонтальная черта',
      },
    ],
    writingNote:
      'Три черты. Сначала дуга сверху вниз с изгибом вправо, потом дуга сверху-справа вниз-влево, в конце — горизонтальная черта.',
  },
  {
    day: 14,
    character: '子',
    meaning: 'ребёнок',
    kunReading: { kana: 'こ', romaji: 'ko' },
    onReading: { kana: 'シ', romaji: 'shi' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '子供', kana: 'こども', romaji: 'kodomo', translation: 'ребёнок, дети' },
      { word: '男の子', kana: 'おとこのこ', romaji: 'otoko no ko', translation: 'мальчик' },
      { word: '息子', kana: 'むすこ', romaji: 'musuko', translation: 'сын' },
    ],
    strokes: [
      {
        d: 'M30.53,17.47c1.69,0.65,3.39,0.79,4.95,0.58c4.54-0.61,25.64-4.2,27.39-4.51c3.17-0.57,3.72,1.25,1.94,3.28c-1.79,2.04-10.47,12.08-15,15.77',
        start: { x: 30.5, y: 17.5 },
        instruction: 'крючок сверху',
      },
      {
        d: 'M48.15,34.62c5.89,2.72,10.78,28.19,4.81,48.23c-2.57,8.61-7.42,2.72-9.61,0.91',
        start: { x: 48.1, y: 34.6 },
        instruction: 'вертикальная, с крючком внизу',
      },
      {
        d: 'M11.24,47.23c3.44,1.05,8.06,0.94,11.45,0.45c15.39-2.27,39.32-5.36,53.7-6.19c3.91-0.23,8.36-0.31,12.03,0.52',
        start: { x: 11.2, y: 47.2 },
        instruction: 'горизонтальная черта снизу',
      },
    ],
    writingNote: 'Три черты. Сначала крючок сверху, потом вертикальная черта с крючком внизу, в конце — горизонтальная черта.',
  },
  {
    day: 15,
    character: '水',
    meaning: 'вода',
    kunReading: { kana: 'みず', romaji: 'mizu' },
    onReading: { kana: 'スイ', romaji: 'sui' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '水曜日', kana: 'すいようび', romaji: 'suiyoubi', translation: 'среда' },
      { word: '水泳', kana: 'すいえい', romaji: 'suiei', translation: 'плавание' },
      { word: 'お水', kana: 'おみず', romaji: 'o-mizu', translation: 'вода (вежливо)' },
    ],
    strokes: [
      {
        d: 'M48.41,13.83c0.99,0.99,1.53,2.28,1.61,5.06c0.37,13.35-0.24,57.03-0.24,61.58c0,8.97-6.9,0.03-8.28-1.12',
        start: { x: 48.4, y: 13.8 },
        instruction: 'вертикальная черта с крючком',
      },
      {
        d: 'M16.06,41.97c1.61,0.57,3.42,0.39,4.82,0C23.74,41.17,33.11,37.61,35.4,36.7s4.1,1.14,3.44,3.21C35.78,49.54,25.92,63.3,17.43,68.58',
        start: { x: 16.1, y: 42.0 },
        instruction: 'короткая черта слева',
      },
      {
        d: 'M74.51,25.23c-0.2,1.15-0.66,2.06-1.39,2.72c-5.17,4.68-11.42,8.97-20.6,12.64',
        start: { x: 74.5, y: 25.2 },
        instruction: 'короткая черта справа сверху',
      },
      {
        d: 'M52.29,42.2c8.09,9.84,17.64,19.69,26.07,25.16c1.98,1.28,4.15,2.75,6.5,3.28',
        start: { x: 52.3, y: 42.2 },
        instruction: 'длинная черта вниз-вправо',
      },
    ],
    writingNote:
      'Четыре черты. Сначала вертикальная черта с крючком по центру, потом короткие черты слева и справа, в конце — длинная черта вниз-вправо.',
  },
  {
    day: 16,
    character: '土',
    meaning: 'земля',
    kunReading: { kana: 'つち', romaji: 'tsuchi' },
    onReading: { kana: 'ド', romaji: 'do' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '土曜日', kana: 'どようび', romaji: 'doyoubi', translation: 'суббота' },
      { word: '土地', kana: 'とち', romaji: 'tochi', translation: 'земля, участок' },
    ],
    strokes: [
      {
        d: 'M24.43,46.69c1.5,0.37,4.26,0.55,5.74,0.37C39.91,45.87,56.99,44.04,69.41,43.05c2.49-0.2,4,0.17,5.25,0.36',
        start: { x: 24.4, y: 46.7 },
        instruction: 'верхняя горизонтальная черта',
      },
      {
        d: 'M47.86,15.94c1.07,1.07,1.85,2.87,1.85,4.26c0,9.4,0.13,56.02,0.13,58.13',
        start: { x: 47.9, y: 15.9 },
        instruction: 'вертикальная, сверху вниз',
      },
      {
        d: 'M14.11,80.49c1.94,0.5,5.51,0.67,7.45,0.5C42.2,79.13,63.3,77.63,82.88,76.87c3.24-0.13,5.18,0.24,6.8,0.49',
        start: { x: 14.1, y: 80.5 },
        instruction: 'нижняя горизонтальная черта, шире',
      },
    ],
    writingNote: 'Три черты. Верхняя горизонтальная, потом вертикальная через середину, в конце — широкая нижняя черта.',
  },
  {
    day: 17,
    character: '金',
    meaning: 'золото, деньги',
    kunReading: { kana: 'かね', romaji: 'kane' },
    onReading: { kana: 'キン', romaji: 'kin' },
    jlptLevel: 'N5',
    strokeCount: 8,
    exampleWords: [
      { word: 'お金', kana: 'おかね', romaji: 'o-kane', translation: 'деньги' },
      { word: '金曜日', kana: 'きんようび', romaji: "kin'youbi", translation: 'пятница' },
      { word: '金魚', kana: 'きんぎょ', romaji: 'kingyo', translation: 'золотая рыбка' },
    ],
    strokes: [
      {
        d: 'M47.48,10.9c0.23,1.39-0.2,3.28-0.73,4.44C43.79,21.83,30.39,43.21,13.3,53.21',
        start: { x: 47.5, y: 10.9 },
        instruction: 'левый скат крыши',
      },
      {
        d: 'M47.94,16.74c8.72,6.88,31.32,28.33,34.14,29.97c2.86,1.67,3.8,2.44,5.08,2.6',
        start: { x: 47.9, y: 16.7 },
        instruction: 'правый скат крыши',
      },
      {
        d: 'M31.21,43.19c1.55,0.6,3.53,0.33,5.14,0.19c6.34-0.55,13.15-1.55,22.01-2.42c1.9-0.18,3.76-0.37,5.64,0.11',
        start: { x: 31.2, y: 43.2 },
        instruction: 'первая горизонтальная черта',
      },
      {
        d: 'M27.69,59.6c1.79,0.61,4.1,0.28,5.94,0.11c8.48-0.8,15.98-1.45,28.76-2.32c2.11-0.15,4.29-0.33,6.39,0.07',
        start: { x: 27.7, y: 59.6 },
        instruction: 'вторая горизонтальная черта',
      },
      {
        d: 'M47.22,44.79c0.82,0.78,0.82,3.45,0.82,4.06c0,3.34,0.25,35.51,0.2,36.53',
        start: { x: 47.2, y: 44.8 },
        instruction: 'вертикальная черта по центру',
      },
      {
        d: 'M28.44,68.58c2.98,2.75,6.86,8.5,7.8,11.01',
        start: { x: 28.4, y: 68.6 },
        instruction: 'короткая черта влево-вниз',
      },
      {
        d: 'M66.98,66.16c0.22,1.05,0.1,2.26-0.5,3.22C64.57,72.48,60.95,76.35,57.8,78.9',
        start: { x: 67.0, y: 66.2 },
        instruction: 'короткая черта вправо-вниз',
      },
      {
        d: 'M16.97,87.03c2.64,0.93,5.88,0.37,8.6,0.14c15.18-1.3,30.23-1.94,47.26-2.75c2.87-0.14,5.8-0.25,8.61,0.54',
        start: { x: 17.0, y: 87.0 },
        instruction: 'нижняя черта, основание',
      },
    ],
    writingNote:
      'Восемь черт. Сначала «крыша» из двух скатов, потом два горизонтальных штриха и вертикаль по центру, затем два коротких штриха по бокам, и в конце — черта-основание внизу.',
  },
  {
    day: 18,
    character: '口',
    meaning: 'рот',
    kunReading: { kana: 'くち', romaji: 'kuchi' },
    onReading: { kana: 'コウ', romaji: 'kou' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '入口', kana: 'いりぐち', romaji: 'iriguchi', translation: 'вход' },
      { word: '出口', kana: 'でぐち', romaji: 'deguchi', translation: 'выход' },
      { word: '人口', kana: 'じんこう', romaji: 'jinkou', translation: 'население' },
    ],
    strokes: [
      {
        d: 'M20.41,30.5c1.15,1.15,1.83,2.64,2.07,4.06c1.06,6.45,2.89,21.66,4.29,34.72C27.03,71.64,27.28,73.94,27.52,76.15',
        start: { x: 20.4, y: 30.5 },
        instruction: 'левая вертикальная черта',
      },
      {
        d: 'M23.2,32.72c16.02-1.99,38.16-4.62,50.91-5.44c3.61-0.23,5.81,2.5,5.25,4.72c-2.06,8.14-6.07,24.31-8.26,35.66',
        start: { x: 23.2, y: 32.7 },
        instruction: 'верх и правая сторона одной чертой',
      },
      {
        d: 'M27.75,71.33c9.63-0.46,28.01-2.11,41.28-2.79c1.88-0.1,3.66-0.17,5.28-0.19',
        start: { x: 27.8, y: 71.3 },
        instruction: 'нижняя черта, закрывает',
      },
    ],
    writingNote: 'Три черты. Левая сторона, затем верх и правая сторона одной чертой, в конце — нижняя черта, закрывает квадрат.',
  },
  {
    day: 19,
    character: '中',
    meaning: 'середина, внутри',
    kunReading: { kana: 'なか', romaji: 'naka' },
    onReading: { kana: 'チュウ', romaji: 'chuu' },
    jlptLevel: 'N5',
    strokeCount: 4,
    exampleWords: [
      { word: '中国', kana: 'ちゅうごく', romaji: 'chuugoku', translation: 'Китай' },
      { word: '中心', kana: 'ちゅうしん', romaji: 'chuushin', translation: 'центр' },
      { word: '中学校', kana: 'ちゅうがっこう', romaji: 'chuugakkou', translation: 'средняя школа' },
    ],
    strokes: [
      {
        d: 'M18.25,33.83c0.92,0.92,1.6,2.06,1.84,3.35c1.04,5.24,2.37,11.98,3.83,21.07c0.25,1.54,0.5,4.06,0.76,5.74',
        start: { x: 18.2, y: 33.8 },
        instruction: 'левая вертикальная черта',
      },
      {
        d: 'M21.4,36.25C34.06,34.51,65.03,31.19,77.06,30.5c4.02-0.23,5.5,1.05,4.7,4.06c-1.4,5.23-5.15,18.51-5.61,20.27',
        start: { x: 21.4, y: 36.2 },
        instruction: 'верх и правая сторона одной чертой',
      },
      {
        d: 'M25.45,59.49C36.81,58.37,56.75,57.06,72.48,55.75c2.17-0.18,5.28-0.25,6.65-0.25',
        start: { x: 25.4, y: 59.5 },
        instruction: 'нижняя черта, закрывает',
      },
      {
        d: 'M48.17,10.55c1.32,1.32,2.06,3.21,2.06,4.64c0,0.83,0.06,51.93-0.14,70.36c-0.03,3.03-0.06,5.14-0.09,5.96',
        start: { x: 48.2, y: 10.6 },
        instruction: 'вертикальная черта через центр',
      },
    ],
    writingNote:
      'Четыре черты. Сначала квадрат — левая сторона, верх с правой стороной одной чертой, нижняя черта, — а в конце вертикальная черта пронзает его насквозь.',
  },
  {
    day: 20,
    character: '上',
    meaning: 'верх',
    kunReading: { kana: 'うえ', romaji: 'ue' },
    onReading: { kana: 'ジョウ', romaji: 'jou' },
    jlptLevel: 'N5',
    strokeCount: 3,
    exampleWords: [
      { word: '上手', kana: 'じょうず', romaji: 'jouzu', translation: 'умелый, искусный' },
      { word: '机の上', kana: 'つくえのうえ', romaji: 'tsukue no ue', translation: 'на столе' },
    ],
    strokes: [
      {
        d: 'M47.99,14.57c1.06,1.06,1.84,2.86,1.84,4.7c0,0.75-0.2,58.37-0.23,59.29',
        start: { x: 48.0, y: 14.6 },
        instruction: 'вертикальная черта',
      },
      {
        d: 'M53.21,41.06c6.42-0.57,13.07-2.29,16.28-2.75c1.27-0.18,3.21-0.35,4.36,0',
        start: { x: 53.2, y: 41.1 },
        instruction: 'короткая горизонтальная черта справа',
      },
      {
        d: 'M12.28,80.99c3.3,1.06,6.83,0.57,10.21,0.31c14.89-1.13,37.76-2.44,55.27-2.68c3.35-0.05,6.85-0.29,10.09,0.75',
        start: { x: 12.3, y: 81.0 },
        instruction: 'нижняя горизонтальная черта, длинная',
      },
    ],
    writingNote: 'Три черты. Вертикальная черта, потом короткая горизонтальная справа, в конце — длинная черта в основании.',
  },
]

export function getKanjiByDay(day: number): Kanji | undefined {
  return KANJI_DATA.find((k) => k.day === day)
}
