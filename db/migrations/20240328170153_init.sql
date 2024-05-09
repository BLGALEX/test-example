-- migrate:up

CREATE TABLE "user" (
    -- common
    id                                  uuid                                                          PRIMARY KEY,
    created_at                          TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc'::TEXT, NOW()) NOT NULL,
    updated_at                          TIMESTAMP WITHOUT TIME ZONE,
    goal_to_learn                       CHARACTER VARYING,
    interests                           CHARACTER VARYING[],
    -- api-service
    name                                CHARACTER VARYING(1000),
    email                               CHARACTER VARYING(1000),
    status                              CHARACTER VARYING,
    language                            CHARACTER VARYING(10),
    goals_to_improve                    CHARACTER VARYING[],
    daily_goal                          CHARACTER VARYING,
    level                               CHARACTER VARYING,
    situations                          CHARACTER VARYING[],
    preferred_accent                    CHARACTER VARYING,
    gender                              CHARACTER VARYING,
    age                                 CHARACTER VARYING,
    selected_course_id                  uuid,
    desired_outcomes                    CHARACTER VARYING[],
    learning_pleasure                   CHARACTER VARYING,
    skill_to_improve                    CHARACTER VARYING,
    fcm_token                           CHARACTER VARYING,
    timezone                            CHARACTER VARYING,
    learning_background                 CHARACTER VARYING[],
    is_onboarding_lesson_screen_passed  BOOLEAN,
    is_personal_plan_screen_passed      BOOLEAN,
    timer_time_mins                     INTEGER,
    timer_reset_interval_mins           INTEGER,
    -- gpt-lessons-service
    default_avatar_id                   uuid,
    cefr_level_extended                 CHARACTER VARYING
);

CREATE INDEX ix_user_updated_at_index ON public."user" USING btree (updated_at);

-- migrate:down

DROP TABLE "user";
