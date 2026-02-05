export class Competence {

  private readonly nom: string;
  private readonly niveau: 'debutant' | 'intermediaire' | 'expert';
  private readonly domaineExpertise: string;

  private constructor(
    nom: string,
    niveau: 'debutant' | 'intermediaire' | 'expert',
    domaineExpertise: string
  ) {
    this.nom = nom;
    this.niveau = niveau;
    this.domaineExpertise = domaineExpertise;
  }

  static creer(
    nom: string,
    niveau: 'debutant' | 'intermediaire' | 'expert',
    domaineExpertise: string
  ): Competence {

    if (!nom || nom.trim().length < 3) {
      throw new Error('Le nom de la compétence doit contenir au moins 3 caractères');
    }

    if (!domaineExpertise || domaineExpertise.trim().length === 0) {
      throw new Error('Le domaine d\'expertise est obligatoire');
    }

    return new Competence(
      nom.trim(),
      niveau,
      domaineExpertise.trim()
    );
  }

  getNom(): string {
    return this.nom;
  }

  getNiveau(): string {
    return this.niveau;
  }

  getDomaineExpertise(): string {
    return this.domaineExpertise;
  }

  equals(other: Competence): boolean {
    if (!other) return false;

    return this.nom === other.nom &&
           this.niveau === other.niveau &&
           this.domaineExpertise === other.domaineExpertise;
  }

  estExpert(): boolean {
    return this.niveau === 'expert';
  }

  memeCompetence(other: Competence): boolean {
    return this.nom.toLowerCase() === other.nom.toLowerCase();
  }
}
