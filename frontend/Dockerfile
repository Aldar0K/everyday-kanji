# Многоступенчатая сборка: собираем бандл в Node, а отдаём статику из nginx.
#
# Отличие от Taska, где рантаймом служит `npm run preview`: preview — это
# сервер Vite для локального просмотра сборки, он однопоточный и не задуман
# для продакшена. К тому же в образ пришлось бы класть весь node_modules и
# исходники — сотни мегабайт против ~50 МБ с nginx.

FROM node:20-alpine AS build

WORKDIR /app

# Зависимости отдельным слоем: пересобираются только при изменении манифестов.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build


FROM nginx:1.27-alpine AS runtime

# Своя конфигурация: SPA должна отдавать index.html на любой неизвестный путь,
# иначе прямой заход на /day/12/strokes вернёт 404.
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
