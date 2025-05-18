--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg120+1)
-- Dumped by pg_dump version 16.9 (Debian 16.9-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    id integer NOT NULL,
    url character varying NOT NULL,
    title character varying,
    price_usd integer,
    odometer integer,
    username character varying,
    phone_number character varying,
    image_url character varying,
    images_count integer,
    car_number character varying,
    car_vin character varying,
    datetime_found timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cars_id_seq OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_id_seq OWNED BY public.cars.id;


--
-- Name: cars id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN id SET DEFAULT nextval('public.cars_id_seq'::regclass);


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (id, url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found) FROM stdin;
1	https://example.com/car/123	Toyota Camry 2012	8500	142000	John Doe	+380999999999	https://example.com/img.jpg	10	AA1234BB	1HGCM82633A123456	2025-05-17 12:19:08.420607+00
67	https://auto.ria.com/uk/auto_bmw_x5_38307784.html	BMW X5 2017	38000	185000	Іван Іванович	+380671110080	https://cdn4.riastatic.com/photosnew/auto/photo/bmw_x5__599110944f.jpg	98	BK8000BB	WBAKS610X00N71352	2025-05-17 13:32:19.041567+00
68	https://auto.ria.com/uk/auto_volkswagen_passat_38307518.html	Volkswagen Passat 2011	8900	243000	Auto	+380967545008	https://cdn1.riastatic.com/photosnew/auto/photo/volkswagen_passat__599105961f.jpg	41	KA4414BA	WVWZZZ3CxBExxxx04	2025-05-17 13:32:24.242767+00
69	https://auto.ria.com/uk/auto_neta_u_pro_400_36871296.html	Neta U Pro 400 2022	14900	50000	\N	+380672117887	https://cdn1.riastatic.com/photosnew/auto/photo/neta_u-pro-400__559249256f.jpg	25	AI0516YA	LUZBGAFB4NA019480	2025-05-17 13:32:29.140272+00
70	https://auto.ria.com/uk/auto_bmw_5_series_37886947.html	BMW 5 Series 2013	14299	184000	Софія	+380674361203	https://cdn3.riastatic.com/photosnew/auto/photo/bmw_5-series__595260638f.jpg	100	BC5746TK	WBA5A7C50ED612201	2025-05-17 13:32:38.589468+00
71	https://auto.ria.com/uk/auto_toyota_corolla_37697615.html	Toyota Corolla 2008	6999	162000	Степан	+380980522183	https://cdn0.riastatic.com/photosnew/auto/photo/toyota_corolla__582112735f.jpg	51	\N	JTNBV58E80J015236	2025-05-17 13:32:44.054919+00
72	https://auto.ria.com/uk/auto_hyundai_santa_fe_38286841.html	Hyundai Santa FE 2011	15500	146000	Максим	+380975177929	https://cdn4.riastatic.com/photosnew/auto/photo/hyundai_santa-fe__598559059f.jpg	69	\N	KMHSH81XDBU780546	2025-05-17 13:32:49.048592+00
73	https://auto.ria.com/uk/auto_mercedes_benz_s_class_38302455.html	Mercedes-Benz S-Class 2017	44900	218000	Mihail Bilanici	+380970343301	https://cdn0.riastatic.com/photosnew/auto/photo/mercedes-benz_s-class__598960425f.jpg	29	AT0044CH	WDDUG6GB2JA356135	2025-05-17 13:32:54.228798+00
74	https://auto.ria.com/uk/auto_skoda_octavia_38284907.html	Skoda Octavia 2020	17300	175000	\N	+380970102233	https://img.youtube.com/vi/23jdeT5IJFc/default.jpg	92	\N	TMBLK7NE2L0034448	2025-05-17 13:33:05.370227+00
75	https://auto.ria.com/uk/auto_mazda_cx_5_38252506.html	Mazda CX-5 2017	21990	157000	Олег	+380673503458	https://cdn0.riastatic.com/photosnew/auto/photo/mazda_cx-5__597623295f.jpg	80	\N	JMZKFGW1600684394	2025-05-17 13:33:11.033125+00
76	https://auto.ria.com/uk/auto_hyundai_santa_fe_37990009.html	Hyundai Santa FE 2013	11600	236000	Slavik	+380679509607	https://cdn1.riastatic.com/photosnew/auto/photo/hyundai_santa-fe__590264561f.jpg	40	CA9403KI	5XYZT3LBXDG075480	2025-05-17 13:33:16.210976+00
\.


--
-- Name: cars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_id_seq', 99, true);


--
-- Name: cars cars_car_vin_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_car_vin_key UNIQUE (car_vin);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (id);


--
-- Name: ix_cars_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cars_id ON public.cars USING btree (id);


--
-- Name: ix_cars_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_cars_url ON public.cars USING btree (url);


--
-- PostgreSQL database dump complete
--

