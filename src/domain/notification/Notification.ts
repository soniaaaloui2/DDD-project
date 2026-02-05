export class Notification {

  private id: string;
  private destinataire: string;
  private sujet: string;
  private message: string;
  private formateurConcerneId: string;
  private statut: 'en_attente' | 'envoyee' | 'echec';
  private dateCreation: Date;
  private dateEnvoi?: Date;

  private constructor(
    id: string,
    destinataire: string,
    sujet: string,
    message: string,
    formateurConcerneId: string
  ) {
    this.id = id;
    this.destinataire = destinataire;
    this.sujet = sujet;
    this.message = message;
    this.formateurConcerneId = formateurConcerneId;
    this.statut = 'en_attente';
    this.dateCreation = new Date();
    this.dateEnvoi = undefined;
  }

  static creer(
    destinataire: string,
    sujet: string,
    message: string,
    formateurConcerneId: string
  ): Notification {

    if (!destinataire || !destinataire.includes('@')) {
      throw new Error('Email destinataire invalide');
    }

    if (!sujet || sujet.trim().length === 0) {
      throw new Error('Le sujet ne peut pas être vide');
    }

    if (!message || message.trim().length === 0) {
      throw new Error('Le message ne peut pas être vide');
    }

    if (!formateurConcerneId || formateurConcerneId.trim().length === 0) {
      throw new Error('L\'ID du formateur concerné est obligatoire');
    }

    const id = `NOTIF-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return new Notification(id, destinataire, sujet, message, formateurConcerneId);
  }

  marquerEnvoyee(): void {
    if (this.statut === 'envoyee') {
      throw new Error('La notification a déjà été envoyée');
    }

    this.statut = 'envoyee';
    this.dateEnvoi = new Date();
  }

  marquerEchec(): void {
    if (this.statut === 'envoyee') {
      throw new Error('Impossible de marquer en échec une notification déjà envoyée');
    }

    this.statut = 'echec';
  }

  reessayerEnvoi(): void {
    if (this.statut !== 'echec') {
      throw new Error('On ne peut réessayer que les notifications en échec');
    }

    this.statut = 'en_attente';
  }


  getId(): string {
    return this.id;
  }

  getDestinataire(): string {
    return this.destinataire;
  }

  getSujet(): string {
    return this.sujet;
  }

  getMessage(): string {
    return this.message;
  }

  getFormateurConcerneId(): string {
    return this.formateurConcerneId;
  }

  getStatut(): string {
    return this.statut;
  }

  getDateCreation(): Date {
    return this.dateCreation;
  }

  getDateEnvoi(): Date | undefined {
    return this.dateEnvoi;
  }

  estEnvoyee(): boolean {
    return this.statut === 'envoyee';
  }

  estEnAttente(): boolean {
    return this.statut === 'en_attente';
  }

  aEchoue(): boolean {
    return this.statut === 'echec';
  }
}
