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
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(128) NOT NULL
);


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone,
    goal_to_learn character varying,
    interests character varying[],
    name character varying(1000),
    email character varying(1000),
    status character varying,
    language character varying(10),
    goals_to_improve character varying[],
    daily_goal character varying,
    level character varying,
    situations character varying[],
    preferred_accent character varying,
    gender character varying,
    age character varying,
    selected_course_id uuid,
    desired_outcomes character varying[],
    learning_pleasure character varying,
    skill_to_improve character varying,
    fcm_token character varying,
    timezone character varying,
    learning_background character varying[],
    is_onboarding_lesson_screen_passed boolean,
    is_personal_plan_screen_passed boolean,
    timer_time_mins integer,
    timer_reset_interval_mins integer,
    default_avatar_id uuid,
    cefr_level_extended character varying
);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_user_updated_at_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_updated_at_index ON public."user" USING btree (updated_at);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20240328170153');
