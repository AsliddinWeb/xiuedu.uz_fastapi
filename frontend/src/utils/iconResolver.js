/**
 * Resolve a heroicon name (string from CMS) to a Vue component.
 * Falls back to a generic placeholder if the name is unknown.
 *
 * Only the icons we actually use on the home page are imported,
 * so the bundle stays small.
 */
import {
  AcademicCapIcon, ArrowRightIcon, ArrowUpRightIcon, BanknotesIcon,
  BeakerIcon, BookOpenIcon, BriefcaseIcon, BuildingLibraryIcon,
  BuildingOffice2Icon, CalendarDaysIcon, CameraIcon, ChartBarIcon,
  ChatBubbleLeftRightIcon, ClipboardDocumentCheckIcon, ClockIcon,
  CodeBracketIcon, ComputerDesktopIcon, CpuChipIcon, DocumentTextIcon,
  GlobeAltIcon, IdentificationIcon, LanguageIcon, LightBulbIcon,
  LockClosedIcon, MagnifyingGlassIcon, MapPinIcon, MegaphoneIcon,
  PaintBrushIcon, PaperAirplaneIcon, PencilSquareIcon, PhoneIcon, PhotoIcon, PlayIcon,
  ScaleIcon, ServerStackIcon, ShieldCheckIcon, SparklesIcon, StarIcon,
  SunIcon, TrophyIcon, UserCircleIcon, UserGroupIcon
} from '@heroicons/vue/24/outline'

const ICONS = {
  AcademicCapIcon, ArrowRightIcon, ArrowUpRightIcon, BanknotesIcon,
  BeakerIcon, BookOpenIcon, BriefcaseIcon, BuildingLibraryIcon,
  BuildingOffice2Icon, CalendarDaysIcon, CameraIcon, ChartBarIcon,
  ChatBubbleLeftRightIcon, ClipboardDocumentCheckIcon, ClockIcon,
  CodeBracketIcon, ComputerDesktopIcon, CpuChipIcon, DocumentTextIcon,
  GlobeAltIcon, IdentificationIcon, LanguageIcon, LightBulbIcon,
  LockClosedIcon, MagnifyingGlassIcon, MapPinIcon, MegaphoneIcon,
  PaintBrushIcon, PaperAirplaneIcon, PencilSquareIcon, PhoneIcon, PhotoIcon, PlayIcon,
  ScaleIcon, ServerStackIcon, ShieldCheckIcon, SparklesIcon, StarIcon,
  SunIcon, TrophyIcon, UserCircleIcon, UserGroupIcon
}

export function resolveIcon(name) {
  return ICONS[name] || SparklesIcon
}
