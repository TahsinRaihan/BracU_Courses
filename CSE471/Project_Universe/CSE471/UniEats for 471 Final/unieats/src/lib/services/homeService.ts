
import * as homeRepository from '../repositories/homeRepository';

export async function getHomePageData() {
  const daily = await homeRepository.getDailyMenuItems();
  const weekly = await homeRepository.getWeeklyMenuItems();

  let pool = [...daily, ...weekly];
  if (!pool.length) {
    const all = await homeRepository.getAllMenuItems();
    pool = all;
  }

  const shuffled = pool.sort(() => 0.5 - Math.random());
  const offers = shuffled.slice(0, 3).map(item => {
    const isBogo = Math.random() < 0.5;
    return {
      ...item,
      title: isBogo
        ? `Buy 1 Get 1 Free on ${item.name}`
        : `${Math.floor(Math.random() * 31) + 20}% Off on ${item.name}`,
      link: `/item/${item.id}`
    };
  });

  return { daily, weekly, offers };
}
