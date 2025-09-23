CREATE TABLE public.alltimeleaderboard (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  userID bigint,
  Score bigint,
  achievedOn timestamp without time zone NOT NULL,
  CONSTRAINT alltimeleaderboard_pkey PRIMARY KEY (id),
  CONSTRAINT alltimeLeaderboard_userID_fkey FOREIGN KEY (userID) REFERENCES public.users(userid)
);
CREATE TABLE public.leaderboard (
  entryId bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  userID bigint UNIQUE,
  score bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT leaderboard_pkey PRIMARY KEY (entryId),
  CONSTRAINT leaderboard_userID_fkey FOREIGN KEY (userID) REFERENCES public.users(userid)
);
CREATE TABLE public.users (
  userid bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  username character varying,
  password character varying,
  email character varying,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (userid)
);

-- Insert mock users
INSERT INTO users (username, password, email, created_at) VALUES
('alice', '$2b$14$6CleSk927aVEm1XixuQmV.kyXmxAMDK0x2ez/P4MgbGT30Qbr9SuK', 'alice@example.com', NOW()), -- password is "hashed_pw_1"
('bob', '$2b$14$7V/kVVnVRm0kGYdclPja6.qIVDJGQnje0./MitcjUQV.kEQ/XvYY2', 'bob@example.com', NOW()), -- password is "hashed_pw_2"
('charlie', '$2b$14$qsgyAIpzmop6El/NI34dP.F1BISRbG7DbM/wVjZBSuAY0fU40yBYu', 'charlie@example.com', NOW()); -- password is "hashed_pw_3"

-- Insert mock leaderboard entries
INSERT INTO leaderboard ("userID", score, created_at) VALUES
((SELECT Userid FROM users WHERE Username = 'alice'), 120, NOW() - INTERVAL '3 days'),
((SELECT Userid FROM users WHERE Username = 'bob'),   200, NOW() - INTERVAL '2 days'),
((SELECT Userid FROM Users WHERE Username = 'charlie'), 90, NOW());

-- Insert mock all-time leaderboard entries
INSERT INTO alltimeleaderboard ("userID", score, achievedon) VALUES
((SELECT Userid FROM users WHERE Username = 'bob'),    200, NOW() - INTERVAL '2 days'),
((SELECT Userid FROM users WHERE Username = 'alice'),  180, NOW() - INTERVAL '1 day'),
((SELECT Userid FROM users WHERE Username = 'charlie'), 90, NOW());
