--
-- PostgreSQL database dump
--

\restrict Oj7PshCVp5i88m8WzXmHBM0pgX0lcQYqr9a1t0zE0BWultmThhfPHt4VXbAukFa

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_category_id_fkey;
ALTER TABLE IF EXISTS ONLY public.cart_items DROP CONSTRAINT IF EXISTS cart_items_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.cart_items DROP CONSTRAINT IF EXISTS cart_items_product_id_fkey;
DROP INDEX IF EXISTS public.ix_products_name;
DROP INDEX IF EXISTS public.ix_online_shop_users_user_id;
DROP INDEX IF EXISTS public.ix_categories_slug;
DROP INDEX IF EXISTS public.ix_categories_name;
DROP INDEX IF EXISTS public.ix_cart_items_user_id;
DROP INDEX IF EXISTS public.ix_cart_items_product_id;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_pkey;
ALTER TABLE IF EXISTS ONLY public.online_shop_users DROP CONSTRAINT IF EXISTS online_shop_users_pkey;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_items DROP CONSTRAINT IF EXISTS cart_items_pkey;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS public.products ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.online_shop_users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.categories ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.cart_items ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.products_id_seq;
DROP TABLE IF EXISTS public.products;
DROP SEQUENCE IF EXISTS public.online_shop_users_id_seq;
DROP TABLE IF EXISTS public.online_shop_users;
DROP SEQUENCE IF EXISTS public.categories_id_seq;
DROP TABLE IF EXISTS public.categories;
DROP SEQUENCE IF EXISTS public.cart_items_id_seq;
DROP TABLE IF EXISTS public.cart_items;
DROP TABLE IF EXISTS public.alembic_version;
DROP TYPE IF EXISTS public.user_rolw_enum;
--
-- Name: user_rolw_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.user_rolw_enum AS ENUM (
    'USER',
    'ADMIN'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cart_items (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    added_at timestamp with time zone DEFAULT now()
);


--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cart_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100),
    is_active boolean,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: online_shop_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.online_shop_users (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    username character varying(50),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    language character varying(10) NOT NULL,
    role public.user_rolw_enum NOT NULL,
    is_alive boolean NOT NULL,
    banned boolean NOT NULL
);


--
-- Name: online_shop_users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.online_shop_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: online_shop_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.online_shop_users_id_seq OWNED BY public.online_shop_users.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(10,2) NOT NULL,
    photo_url character varying(500),
    category_id integer,
    is_available boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: online_shop_users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.online_shop_users ALTER COLUMN id SET DEFAULT nextval('public.online_shop_users_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
c974b9f93f6f
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cart_items (id, user_id, product_id, quantity, added_at) FROM stdin;
16	5873099605	12	1	2025-09-23 22:30:08.514354+07
15	5873099605	2	1	2025-09-21 13:24:56.311217+07
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (id, name, slug, is_active, created_at) FROM stdin;
1	Напитки	drinks	t	2025-09-15 13:47:29.634089+07
2	Алкоголь	alcohol	t	2025-09-15 13:47:29.634089+07
3	Сигареты	cigarettes	t	2025-09-15 13:47:29.634089+07
4	Чай / кофе	tea	t	2025-09-15 13:47:29.634089+07
5	Крупы	cereals	t	2025-09-15 13:47:29.634089+07
6	Полуфабрикаты	semi_finished_products	t	2025-09-15 13:47:29.634089+07
7	Консервы	canned_goods	t	2025-09-15 13:47:29.634089+07
8	Лапша / Макароны	noodles	t	2025-09-15 13:47:29.634089+07
9	Хлеб	bread	t	2025-09-15 13:47:29.634089+07
10	Масло	butter	t	2025-09-15 13:47:29.634089+07
11	Овощи	vegetables	t	2025-09-15 13:47:29.634089+07
\.


--
-- Data for Name: online_shop_users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.online_shop_users (id, user_id, username, created_at, language, role, is_alive, banned) FROM stdin;
1	8084334783	\N	2025-09-12 20:48:03.327052+07	ru	ADMIN	t	f
2	5873099605	SibAlive	2025-09-15 11:34:10.879117+07	ru	USER	t	f
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (id, name, price, photo_url, category_id, is_available, created_at, updated_at) FROM stdin;
11	Lucky strike original blue	13000.00	AgACAgIAAxkBAAIX8mjHute2pP6mtND5cDNGUhHyoHe0AAI49DEbpxBBSlJu4X00AAFUmwEAAwIAA20AAzYE	3	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
6	Виски Johnny Walker Red label 40% 500ml	550000.00	AgACAgIAAxkBAAIXvWjHuAABPWWYwCpBSKYTQn38IJS-3AAC6PMxG6cQQUpBsj5GyuP6vwEAAwIAA3kAAzYE	2	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
7	Виски White Horse 40% 750ml	800000.00	AgACAgIAAxkBAAIXxGjHuUyEN57LjRPMo-Ot4CaQ-KvBAAL08zEbpxBBSupXWtmmtfUGAQADAgADeAADNgQ	2	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
8	Водка Ташкент 500ml	55000.00	AgACAgIAAxkBAAIXwmjHuT_2DFLFmAABzZicHIHjyTQQ8gAC8_MxG6cQQUq8n6f6FHBmfwEAAwIAA3gAAzYE	2	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
26	Буханка хлеба 400 гр	3000.00	AgACAgIAAxkBAAIXxmjHuWAhjkPa-Gr8U9hJyjA6XSxkAAL18zEbpxBBSomHo7KosHurAQADAgADeAADNgQ	9	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
27	Патыр 500 гр	6000.00	AgACAgIAAxkBAAIXymjHuXp3ngY3xN6O1-5zYyxEq1qqAAL38zEbpxBBSt1tU66VL7X-AQADAgADeAADNgQ	9	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
28	Патыр 350 гр	4000.00	AgACAgIAAxkBAAIXyGjHuW6ozhgxynO3bdrsnPKaxncFAAL28zEbpxBBSkCGCNbbK-QlAQADAgADbQADNgQ	9	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
29	Масло хлопковое рафинированное Lazzat 1000 мл	14000.00	AgACAgIAAxkBAAIXzGjHuYwY5nb_4Rr2x4sjy4Js3gw0AAL48zEbpxBBSolq5vVEEG4tAQADAgADeQADNgQ	10	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
30	Масло растительное Щедрое лето 1 л.	20000.00	AgACAgIAAxkBAAIXzmjHuaPA39xnBRV1nNaOa68P5p-xAAIF9DEbpxBBSsC3IHCo7hSrAQADAgADeQADNgQ	10	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
15	Сахар песок 1 кг	12000.00	AgACAgIAAxkBAAIX3GjHukaC5QRajSrY-HmGFiufRwtTAAIl9DEbpxBBSnmocUXd5IuDAQADAgADbQADNgQ	5	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
16	Рис Аланга 1 кг	12000.00	AgACAgIAAxkBAAIX2GjHujDSlrWt3o8Gv-d7iXQiOJdCAAIi9DEbpxBBShw-2w26Lk1oAQADAgADbQADNgQ	5	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
17	Гречка 1 кг	15000.00	AgACAgIAAxkBAAIX1mjHuh5vCuH4Roo215VAPfRy7AjPAAIh9DEbpxBBShQf70DBXL9zAQADAgADbQADNgQ	5	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
18	Соль крупная йодированная 1 кг	3000.00	AgACAgIAAxkBAAIX2mjHujyyR1bTFd57TOwqUOJBdk8yAAIk9DEbpxBBSkaZddnQf43sAQADAgADbQADNgQ	5	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
21	Алтайская говядина 525 гр	55000.00	AgACAgIAAxkBAAIX0mjHuesZnsfUyNosfn6InEPP7mu3AAIR9DEbpxBBSgxZMTxDYmrLAQADAgADbQADNgQ	7	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
22	Сардинелла Kaija 240 гр	18000.00	AgACAgIAAxkBAAIX0GjHubHVszXqkqbJr3OX8NitoUedAAIG9DEbpxBBShWh7LxtiqxyAQADAgADbQADNgQ	7	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
23	Килька балтийская 240 гр	10000.00	AgACAgIAAxkBAAIX1GjHuhEpCLNmtaef3bwWledFZIYGAAIg9DEbpxBBSnP3DaEn2WxKAQADAgADbQADNgQ	7	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
2	Fanta 1.5 литра	14000.00	AgACAgIAAxkBAAIX4GjHumC0uibmpLKG-Wdf3THEz7qsAAIn9DEbpxBBSiQBO9N_7JxHAQADAgADeAADNgQ	1	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
3	Pepsi 1.5 литра	13000.00	AgACAgIAAxkBAAIX5mjHuoHpXfY3DAJyGkEyPFh3C9wIAAIr9DEbpxBBSg8rZALgJY_KAQADAgADbQADNgQ	1	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
4	Минеральная вода Hydrolife 1.5 литра	3000.00	AgACAgIAAxkBAAIX4mjHumnu571QbM3JHGuTxEXxL2gUAAIo9DEbpxBBSsytp194OPm9AQADAgADeQADNgQ	1	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
5	Квас Боярский 1.5 литра	6000.00	AgACAgIAAxkBAAIX5GjHunUaRX22WsCpKPBXxVLS3iigAAIp9DEbpxBBSuvgqaud0XiBAQADAgADeAADNgQ	1	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
9	Pall Mall синий	13000.00	AgACAgIAAxkBAAIX9GjHuuYrwhVfv9j6amjkbeSe185GAAI69DEbpxBBSviy0ArSr9pUAQADAgADeAADNgQ	3	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
10	Kent Original	20000.00	AgACAgIAAxkBAAIX8GjHusdtW-FTQQOuTgdoBdsNo6CqAAI39DEbpxBBStsqE-D4ldiyAQADAgADeAADNgQ	3	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
12	Maccoffee original 150 гр	45000.00	AgACAgIAAxkBAAIX-mjHuxWRfWf7RfI3D_ahoOJroNTNAAI99DEbpxBBShBma4geht2kAQADAgADeQADNgQ	4	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
13	Кофе Jacobs Monarch 500 гр	150000.00	AgACAgIAAxkBAAIX-GjHuwcShCsrXcwXom-szKyNTJiMAAI89DEbpxBBSjawRVCqV2ydAQADAgADbQADNgQ	4	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
14	Чай Ташкент черный оригинальный 100 гр	13000.00	AgACAgIAAxkBAAIX9mjHuvQt_kbQmYpO1KcPZ6pyn0QgAAI79DEbpxBBSnY2dXtybBk-AQADAgADbQADNgQ	4	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
19	Пельмени Makiz из говядины 500 гр	20000.00	AgACAgIAAxkBAAIX6mjHupxxzmEIqhRGbPl2s7kqfh_KAAIy9DEbpxBBSoaSfwFpH-6JAQADAgADeAADNgQ	6	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
20	Котлеты из мраморной говядины 500 гр	55000.00	AgACAgIAAxkBAAIX6GjHuo8AARtRlYzivgJl7WOhjvfYTgACMfQxG6cQQUqSlhdKtwXSNAEAAwIAA3kAAzYE	6	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
24	Макароны макфа 400 гр	8000.00	AgACAgIAAxkBAAIX7mjHurnW53vHhUVBfWTp_EhYPStkAAI09DEbpxBBSrRJWopeP7ewAQADAgADeQADNgQ	8	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
25	Лапша Doshirak говядина 90 гр	7000.00	AgACAgIAAxkBAAIX7GjHuq4zGCrGgcuK9J-FsReOLA11AAIz9DEbpxBBSokpqLFGpaDuAQADAgADbQADNgQ	8	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
31	Картофель 1 кг	5000.00	AgACAgIAAxkBAAIX_2jHuzuz61lDEGQvQDtVaqUGmPMFAAJC9DEbpxBBSmVzA-yAoMzPAQADAgADeAADNgQ	11	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
32	Морковь желтая 1 кг	6000.00	AgACAgIAAxkBAAIX_GjHuyFUPdeK9NdY2nUl9TFopnnXAAJA9DEbpxBBSnxH8Uhdemh2AQADAgADbQADNgQ	11	t	2025-09-15 13:47:29.641161+07	2025-09-15 13:47:29.641161+07
1	Coca-Cola 1.5 литра	12000.00	AgACAgIAAxkBAAIX3mjHulKPuInZ06z2M8z7qEm9jUj6AAIm9DEbpxBBSs2DZvn2o8oPAQADAgADbQADNgQ	1	t	2025-09-15 13:47:29.641161+07	2025-09-17 16:58:41.172616+07
33	Лапша Роллтон 70 гр	5000.00	AgACAgIAAxkBAAIZ22jKhqXEeE9AqPXV4rEAAZ_rUOMKmQACG_UxG2kmWEpMSQhJnRmmogEAAwIAA3gAAzYE	8	t	2025-09-17 17:01:03.106786+07	2025-09-17 17:02:21.029384+07
\.


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 16, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categories_id_seq', 12, true);


--
-- Name: online_shop_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.online_shop_users_id_seq', 3, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 36, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: online_shop_users online_shop_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.online_shop_users
    ADD CONSTRAINT online_shop_users_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: ix_cart_items_product_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cart_items_product_id ON public.cart_items USING btree (product_id);


--
-- Name: ix_cart_items_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cart_items_user_id ON public.cart_items USING btree (user_id);


--
-- Name: ix_categories_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_categories_name ON public.categories USING btree (name);


--
-- Name: ix_categories_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_categories_slug ON public.categories USING btree (slug);


--
-- Name: ix_online_shop_users_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_online_shop_users_user_id ON public.online_shop_users USING btree (user_id);


--
-- Name: ix_products_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_products_name ON public.products USING btree (name);


--
-- Name: cart_items cart_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.online_shop_users(user_id) ON DELETE CASCADE;


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict Oj7PshCVp5i88m8WzXmHBM0pgX0lcQYqr9a1t0zE0BWultmThhfPHt4VXbAukFa

