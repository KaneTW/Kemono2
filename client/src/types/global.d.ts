interface KemonoAPI {
  errors: Map<string, string>,
  favorites: KemonoAPI.Favorites,
  posts: KemonoAPI.Posts
  api: KemonoAPI.API
}

namespace KemonoAPI {
  interface Favorites {
    retrieveFavoriteArtists: () => Promise<string>,
    favoriteArtist: (service: string, id: string) => Promise<boolean>,
    unfavoriteArtist: (service: string, id: string) => Promise<boolean>,
    retrieveFavoritePosts: () => Promise<string>,
    favoritePost: (service: string, user: string, post_id: string) => Promise<boolean>,
    unfavoritePost: (service: string, user: string, post_id: string) => Promise<boolean>
  }

  namespace Favorites {
    interface Artist {
      id: string
      name: string
      service: string
      faved_seq: number
      indexed: string
      updated: string
    }

    interface Post {
      id: string
      service: string
      title: string
      user: string
      added: string
      published: string
      attachments: string[]
      content: string
      edited: null
      embed: {}
      faved_seq: number
      file: {}
      shared_file: boolean
    }
  }

  interface Posts {
    attemptFlag: (service: string, user: string, post_id: string) => Promise<boolean>
  }

  interface API {
    bans: () => Promise<API.BanItem[]>
    bannedArtist: (id:string, service:string) => Promise<API.BannedArtist>
  }

  namespace API {
    interface BanItem {
      id: string
      service: string
    }

    interface BannedArtist {
      name: string
    }
  }
}
