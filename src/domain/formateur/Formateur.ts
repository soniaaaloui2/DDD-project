import { Competence } from './Competence';
import { Justificatif } from './Justificatif';

export class Formateur {

  private id: string;
  private email: string;
  private nomComplet: string;

  private competences: Competence[];
  private justificatifs: Justificatif[];

  private statut: 'en_attente' | 'valide' | 'refuse';
  private dateCreation: Date;


  private constructor(
    id: string,
    email: string,
    nomComplet: string,
    competences: Competence[],
    justificatifs: Justificatif[]
  ) {
    this.id = id;
    this.email = email;
    this.nomComplet = nomComplet;
    this.competences = competences;
    this.justificatifs = justificatifs;
    this.statut = 'en_attente';
    this.dateCreation = new Date();
  }


  static creer(
    email: string,
    nomComplet: string,
    competences: Competence[],
    justificatifs: Justificatif[]
  ): Formateur {

    if (!email || !email.includes('@')) {
      throw new Error('Email invalide');
    }

    if (!nomComplet || nomComplet.trim().length < 2) {
      throw new Error('Le nom doit contenir au moins 2 caractères');
    }

    if (!competences || competences.length === 0) {
      throw new Error('Le formateur doit avoir au moins une compétence');
    }

    if (competences.length > 10) {
      throw new Error('Maximum 10 compétences autorisées');
    }

    if (!justificatifs || justificatifs.length === 0) {
      throw new Error('Le formateur doit fournir au moins un justificatif');
    }

    const id = `FORM-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return new Formateur(id, email, nomComplet, competences, justificatifs);
  }

  ajouterCompetence(competence: Competence): void {
    if (this.competences.length >= 10) {
      throw new Error('Maximum 10 compétences autorisées');
    }

    const existe = this.competences.some(c => c.memeCompetence(competence));
    if (existe) {
      throw new Error('Cette compétence existe déjà');
    }

    this.competences.push(competence);
  }

  ajouterJustificatif(justificatif: Justificatif): void {
    this.justificatifs.push(justificatif);
  }


  valider(): void {
    if (this.statut === 'valide') {
      throw new Error('Le compte est déjà validé');
    }
    this.statut = 'valide';
  }

  refuser(): void {
    if (this.statut === 'refuse') {
      throw new Error('Le compte est déjà refusé');
    }
    this.statut = 'refuse';
  }

  getId(): string {
    return this.id;
  }

  getEmail(): string {
    return this.email;
  }

  getNomComplet(): string {
    return this.nomComplet;
  }

  getCompetences(): Competence[] {
    return [...this.competences];
  }

  getJustificatifs(): Justificatif[] {
    return [...this.justificatifs];
  }

  getStatut(): string {
    return this.statut;
  }

  getDateCreation(): Date {
    return this.dateCreation;
  }

  estEnAttente(): boolean {
    return this.statut === 'en_attente';
  }

  estValide(): boolean {
    return this.statut === 'valide';
  }

  nombreCompetencesExpertes(): number {
    return this.competences.filter(c => c.estExpert()).length;
  }

  aDiplome(): boolean {
    return this.justificatifs.some(j => j.estDiplome());
  }
}
