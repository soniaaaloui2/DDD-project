export class Justificatif {

  private readonly type: 'diplome' | 'certificat' | 'experience';
  private readonly titre: string;
  private readonly dateObtention: Date;
  private readonly urlDocument?: string;

  private constructor(
    type: 'diplome' | 'certificat' | 'experience',
    titre: string,
    dateObtention: Date,
    urlDocument?: string
  ) {
    this.type = type;
    this.titre = titre;
    this.dateObtention = dateObtention;
    this.urlDocument = urlDocument;
  }

  static creer(
    type: 'diplome' | 'certificat' | 'experience',
    titre: string,
    dateObtention: Date,
    urlDocument?: string
  ): Justificatif {

    if (!titre || titre.trim().length === 0) {
      throw new Error('Le titre du justificatif est obligatoire');
    }

    if (dateObtention > new Date()) {
      throw new Error('La date d\'obtention ne peut pas être dans le futur');
    }

    return new Justificatif(
      type,
      titre.trim(),
      dateObtention,
      urlDocument
    );
  }

  getType(): string {
    return this.type;
  }

  getTitre(): string {
    return this.titre;
  }

  getDateObtention(): Date {
    return this.dateObtention;
  }

  getUrlDocument(): string | undefined {
    return this.urlDocument;
  }

  equals(other: Justificatif): boolean {
    if (!other) return false;

    return this.type === other.type &&
           this.titre === other.titre &&
           this.dateObtention.getTime() === other.dateObtention.getTime();
  }

  estRecent(): boolean {
    const cinqAnsEnMs = 5 * 365 * 24 * 60 * 60 * 1000;
    const maintenant = new Date().getTime();
    const dateObtention = this.dateObtention.getTime();

    return (maintenant - dateObtention) < cinqAnsEnMs;
  }

  estDiplome(): boolean {
    return this.type === 'diplome';
  }
}
