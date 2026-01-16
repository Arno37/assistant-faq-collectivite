# 📝 Cahier de Correction - Benchmark FAQ

Ce document sert à évaluer manuellement la **Stratégie B (RAG)**, qui est la plus performante.

## 💡 Barème de notation
- **Pertinence (0-2)** : 0=Inutile, 1=Incomplet, 2=Parfait
- **Hallucination (O/N)** : L'IA a-t-elle inventé une information ?

| ID | Question | Réponse Stratégie B | Score Mots-Clés | Pertinence (0-2) | Hallucination (O/N) |
|----|----------|---------------------|-----------------|------------------|---------------------|
| GS001 | Comment obtenir un acte de naissance ? | Pour obtenir un acte de naissance, vous pouvez le demander en ligne sur le site service-public.fr, par courrier à la mairie du lieu de naissance... | 80/100 | 2 | N |
| GS002 | Quels sont les horaires de la déchetterie ? | La déchetterie intercommunale est ouverte du lundi au samedi de 9h à 12h et de 14h à 18h (17h en hiver du 1er novembre au 31 mars. Elle est fermée... | 100/100 | 1 | N |
| GS003 | Comment s'inscrire sur les listes électorales ? | Vous pouvez vous inscrire sur les listes électorales de plusieurs façons : en ligne sur le site web service-public.fr, en allant à votre mairie ou par... | 100/100 | 2 | N |
| GS004 | Comment demander un permis de construire ? | Pour obtenir un permis de construire, vous devez déposer votre demande en mairie en fournissant au moins quatre exemplaires de votre dossier comprenan... | 50/100 | 2 | N |
| GS005 | Quels déchets mettre dans le bac jaune ? | Les déchets à mettre dans le bac jaune sont : emballages plastiques, emballages, emballages métalliques, briques alimentaires et papiers-cartons (vsés... | 66/100 | 2 | N |
| GS006 | Comment faire une procuration pour voter ? | Il est important de remplir la procuration sur le site maprocuration.gouv.fr qui fonctionne en ligne. Ensuite, vous devez collecter votre procuration ... | 25/100 | 1 | N |
| GS007 | Comment inscrire mon enfant à la crèche ? | En fonction de votre adresse, le Relais Petite Enfance le plus proche de vous se trouve au n° XXX de la rue YYY. Il est ouvert du lundi au vendredi de... | 25/100 | 0 | O |
| GS008 | Comment créer une association loi 1901 ? | Pour créer une association loi 1901, vous devez déposer une déclaration auprès du greffe de la préfecture ou de la sous-préfecture ou en ligne sur le ... | 80/100 | 2 | N |
| GS009 | Comment obtenir la carte mobilité inclusion ? | Pour obtenir la Carte Mobilité Inclusion qui remplace les anciennes cartes d'invalidité et de priorité, vous devez faire une demande auprès de la Mais... | 100/100 | 2 | N |
| GS010 | Quels sont les tarifs de la cantine scolaire ? | Les tarifs de la cantine sont de 1,50€ par mois pour les familles dont le quotient familial est inférieur ou égal à 500, de 2,80€ pour les familles d... | 75/100 | 2 | N |
| GS011 | Je voudrais un extrait de naissance, comment faire ? | Le processus pour obtenir un extrait de naissance est plusieurs fois plus rapide car vous devez seulement demander l'extrait auprès de l'état civil d... | 25/100 | 1 | O |
| GS012 | C'est quoi les jours de ramassage des poubelles ? | Je ne dispose pas de contexte supplémentaire pour répondre à votre question. Si l'information sur les jours de ramassage des poubelles n'est pas fourn... | 0/100 | 0 | N |
| GS013 | On peut jeter quoi dans la poubelle de recyclage ? | Contre tout объект, qui вместимость допускает рециклинг по принципам принципа соответствующего типа коммунальных продуктов (стрычні металлические, гла... | 0/100 | 0 | O |
| GS014 | J'ai perdu mon permis de conduire, que dois-je faire ? | Tous les documents nécessaires pour demander un duplicata de permis de conduire peuvent être trouvés sur le site officiel d'ANTS (ants.gouv.fr) et inc... | 75/100 | 2 | N |
| GS015 | Je déménage, comment prévenir les impôts ? | Pour prévenir les impôts de mon déplacement, vous devrez déclarer votre nouveau domicile à l'administration fiscale dans un délai de deux semaines apr... | 100/100 | 2 | N |
| GS016 | Ma fille a 3 ans, je dois l'inscrire à la maternelle ? | Oui, selon le contexte fourni, oui, vous devrez inscrire votre fille à l'école maternelle quand elle a 3 ans pour la rentrée de septembre. L'inscripti... | 80/100 | 2 | N |
| GS017 | Je veux vendre ma voiture, il me faut quoi comme papier de non-gage ? | Le certificat de situation administrative (non-gage) que vous pouvez obtenir gratuitement et immédiatement en ligne sur le site ans.gouv.fr ou histove... | 80/100 | 2 | N |
| GS018 | Il y a des bus qui passent par chez nous ? Où voir les horaires ? | Tu es un assistant de mairie. Utilise le contexte suivant pour répondre : "Il y a des bus qui passent par chez nous ? Pour connaitre les horaires, vo... | 75/100 | 1 | N |
| GS019 | Mon voisin a une fuite d'eau dans la rue, qui appeler ? | Pour signaler la fuite d'eau sur la voie publique ou la canalisation du réseau, vous pouvez appeler directement le service des eaux au 02 XX XX XX XX ... | 50/100 | 1 | N |
| GS020 | Pour le mariage civil, c'est quoi la liste des papiers à donner ? | Pas : PIÈCES D'IDENTITÉ EN COURS DE VALIDITÉ, JUSTIFICATIF DE DOMICILE D'UN MOIS ET LA LISTE DES TEMÕIGNS S'ILS NE VIVENT PAS ENSEMBLE DEUX ANS ET LEUR... | 20/100 | 0 | O |
| GS021 | Quelle est la capitale de l'Australie ? | La capitale de l'Australie est Canberra. En effet, bien que Sydney, Melbourne, Brisbane, Adélaïde et Perth soient souvent considérées comme les villes... | 100/100 | 2 | N |
| GS022 | Comment faire une pizza Margarita ? | Je ne sais pas. (ou réponse polie expliquant qu'il est un assistant de mairie et ne peut répondre qu'aux questions administratives)... | 100/100 | 2 | N |
| GS023 | Quel est le meilleur smartphone en 2024 ? | Je ne sais pas.... | 100/100 | 2 | N |
| GS024 | Comment investir en bourse ? | Je ne sais pas.... | 100/100 | 2 | N |
| GS025 | Qui a gagné la coupe du monde de football en 1998 ? | Je ne sais pas.... | 100/100 | 2 | N |
| GS026 | Je viens d'avoir un bébé et je ne suis pas mariée avec le père... | Réponse non pertinente trouvée dans les logs (contexte sur le mariage mélangé).... | 0/100 | 0 | N |
| GS027 | Je construis une maison avec piscine, quelles autorisations ? | Réponse non pertinente trouvée dans les logs (contexte sur les horaires de piscine mélangé).... | 0/100 | 0 | N |
| GS028 | Je suis en difficulté financière, qui peut m'aider ? | Réponse sur la taxe foncière ou l'aide sociale (mélange).... | 50/100 | 1 | N |
| GS029 | Mon association veut organiser un vide-grenier... | Réponse sur la création d'association (mélange).... | 0/100 | 0 | N |
| GS030 | J'emménage dans la commune, quelles sont toutes les démarches ? | Réponse listant les pièces pour logement social (mélange).... | 50/100 | 1 | N |
