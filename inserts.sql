-- Aplicações distribuídas - Projeto 3 - setup_and_insert.py
-- Grupo: 20
-- Alunos: 43551 45802 43304

INSERT INTO utilizadores (id, nome, username, password) VALUES
    (1, 'um', 'userUm', 'UmaPass'),
    (2, 'dos', 'userDos', 'DosPass'),
    (3, 'three', 'userThree', 'ThreePass');

INSERT INTO bandas (id, nome, ano, genero) VALUES (2, 'BADBADNOTGOOD', 2011, 'Post-bop, Jazz, Electronica');
INSERT INTO bandas (id, nome, ano, genero) VALUES (3, 'Sam The Kid', 1999, 'Rap, Hip-Hop');
INSERT INTO bandas (id, nome, ano, genero) VALUES (4, 'Daniela Mercury', 1986, 'Axé');
INSERT INTO bandas (id, nome, ano, genero) VALUES (5, 'Ross From Friends', 2016, 'Lo-Fi');

INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (1, 2, 'BBNG2', 2012);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (2, 3, 'Beats Vol.1', 2002);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (3, 4, 'Feijão com Arroz', 1996);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (4, 5, 'You''ll Understand', 2017);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (5, 2, 'III', 2014);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (6, 2, 'IV', 2016);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (7, 2, 'BBNG', 2011);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (8, 3, 'Pratica(mente)', 2006);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (9, 4, 'Música de Rua', 1994);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (10, 5, 'Don''t Sleep, There Are Snakes', 2017);
INSERT INTO albuns (id, id_banda, nome, ano_album) VALUES (11, 1, 'Dsdsasdasd', 22323237);

INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (1, 3, 4);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (2, 2, 3);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (1, 3, 5);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (3, 4, 1);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (3, 11, 4);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (2, 8, 3);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (1, 7, 2);
INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES (3, 9, 2);